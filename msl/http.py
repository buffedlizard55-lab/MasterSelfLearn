"""HTTP layer.  Standard library only; every response becomes an ``Evidence`` row.

The rule this module exists to enforce: a fetch either returns bytes or it returns
a recorded failure.  It never returns ``None`` that a caller might mistake for
"empty data", and it never retries silently past the point where the operator has
told us to stop.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import ssl
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from . import config


_LAST_REQUEST_BY_HOST: Dict[str, float] = {}
_PACE_LOCK = threading.Lock()

# These statuses establish that the generated request was unusable, not that the
# remote service is unavailable. Keep this policy shared by cycle and daily probe.
CALLER_FAULT_STATUSES = frozenset({400, 404, 405, 422})


def _pace(url: str) -> None:
    """Honor a host operator's minimum interval across all callers in-process."""
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    minimum = float(config.HOST_MIN_INTERVAL_SECONDS.get(host, 0.0))
    if minimum <= 0:
        return
    with _PACE_LOCK:
        now = time.monotonic()
        wait = minimum - (now - _LAST_REQUEST_BY_HOST.get(host, 0.0))
        if wait > 0:
            time.sleep(wait)
        _LAST_REQUEST_BY_HOST[host] = time.monotonic()


@dataclass
class FetchResult:
    """The complete, auditable record of one outbound read."""

    url: str
    status: Optional[int] = None
    body: bytes = b""
    error: Optional[str] = None
    error_kind: Optional[str] = None
    elapsed_ms: int = 0
    attempts: int = 0
    rate_limited: bool = False
    final_url: str = ""
    content_type: str = ""
    #: True when the response exceeded MAX_RESPONSE_BYTES. A truncated body is
    #: never parseable evidence, even if its HTTP status was 200.
    truncated: bool = False

    @property
    def ok(self) -> bool:
        return (self.status is not None and 200 <= self.status < 300
                and not self.truncated)

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.body).hexdigest()

    @property
    def size(self) -> int:
        return len(self.body)

    def text(self) -> str:
        return self.body.decode("utf-8", "replace")

    def json(self) -> Any:
        """Parse strict JSON, or raise; NaN/Infinity are not JSON values."""
        def reject_constant(token: str) -> None:
            raise ValueError(f"non-JSON numeric constant {token}")
        return json.loads(self.text(), parse_constant=reject_constant)

    def describe_error(self) -> str:
        return f"{self.error_kind or 'unknown'}: {self.error or ''}".strip()


def health_inconclusive_reason(result: FetchResult) -> str:
    """Why this read cannot support a verdict about source availability.

    A TLS egress policy is about the runner, selected 4xx statuses are about the
    caller-generated URL, and ``ResponseTooLarge`` is this engine's own cap.
    """
    if result.ok:
        return ""
    if result.error_kind == "EgressBlocked":
        return "runner-egress"
    if result.status in CALLER_FAULT_STATUSES:
        return "caller-request"
    if result.error_kind == "ResponseTooLarge":
        return "local-response-cap"
    return ""


@dataclass
class FetchStats:
    """Per-cycle network accounting, surfaced on the site and in the cycle log."""

    requests: int = 0
    ok: int = 0
    failed: int = 0
    bytes_in: int = 0
    ms_total: int = 0
    rate_limited: int = 0
    by_host: Dict[str, int] = field(default_factory=dict)

    def record(self, r: FetchResult) -> None:
        self.requests += 1
        self.ms_total += r.elapsed_ms
        self.bytes_in += r.size
        host = urllib.parse.urlsplit(r.url).netloc or "?"
        self.by_host[host] = self.by_host.get(host, 0) + 1
        if r.ok:
            self.ok += 1
        else:
            self.failed += 1
        if r.rate_limited:
            self.rate_limited += 1

    def as_dict(self) -> Dict[str, Any]:
        return {
            "requests": self.requests,
            "ok": self.ok,
            "failed": self.failed,
            "bytesIn": self.bytes_in,
            "msTotal": self.ms_total,
            "rateLimited": self.rate_limited,
            "byHost": dict(sorted(self.by_host.items(), key=lambda kv: -kv[1])),
        }


def _decompress(res: Any, body: bytes) -> bytes:
    enc = (res.headers.get("Content-Encoding") or "").lower()
    if "gzip" in enc:
        try:
            return gzip.decompress(body)
        except OSError:
            return body
    if "deflate" in enc:
        try:
            return zlib.decompress(body)
        except zlib.error:
            try:
                return zlib.decompress(body, -zlib.MAX_WBITS)
            except zlib.error:
                return body
    return body


def fetch(url: str, headers: Optional[Dict[str, str]] = None,
          timeout: Optional[int] = None, max_bytes: Optional[int] = None,
          retries: Optional[int] = None, accept: Optional[str] = None) -> FetchResult:
    """Read ``url``.  Returns a FetchResult whether or not the read succeeded."""
    hdrs = {"User-Agent": config.USER_AGENT, "Accept-Encoding": "gzip, deflate"}
    if accept:
        hdrs["Accept"] = accept
    hdrs.update(headers or {})

    tries = config.HTTP_RETRIES if retries is None else retries
    limit = config.MAX_RESPONSE_BYTES if max_bytes is None else max_bytes
    res = FetchResult(url=url, final_url=url)
    ctx = ssl.create_default_context()

    for attempt in range(1, tries + 1):
        res.attempts = attempt
        t0 = time.monotonic()
        try:
            _pace(url)
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout or config.HTTP_TIMEOUT,
                                        context=ctx) as r:
                raw = r.read(limit + 1)
                res.status = r.status
                res.content_type = r.headers.get("Content-Type") or ""
                res.final_url = r.geturl() or url
                decoded = _decompress(r, raw)
                res.truncated = len(decoded) > limit
                res.body = decoded[:limit]
                res.elapsed_ms = int((time.monotonic() - t0) * 1000)
                if res.truncated:
                    res.error_kind = "ResponseTooLarge"
                    res.error = (f"response exceeded the {limit}-byte safety cap; "
                                 "the truncated body was not accepted as evidence")
                else:
                    res.error = None
                    res.error_kind = None
                return res
        except urllib.error.HTTPError as e:
            res.status = e.code
            res.error_kind = "HTTPError"
            res.error = f"HTTP {e.code} {e.reason}"
            # 429 has standard rate-limit semantics. A generic 403 is merely
            # forbidden; call it rate-limited only when operator headers say so.
            err_headers = e.headers or {}
            res.rate_limited = (
                e.code == 429 or
                (e.code == 403 and
                 (str(err_headers.get("X-RateLimit-Remaining", "")) == "0" or
                  bool(err_headers.get("Retry-After"))))
            )
            try:
                res.body = e.read(limit)[:limit]
            except Exception:
                res.body = b""
            res.content_type = err_headers.get("Content-Type") or ""
            # Retrying a caller error cannot repair the request and rapidly
            # retrying 403/429 is exactly what operators ask clients not to do.
            # A later scheduled cycle is the safe retry for every HTTP 4xx.
            if 400 <= e.code < 500:
                res.elapsed_ms = int((time.monotonic() - t0) * 1000)
                return res
        except urllib.error.URLError as e:
            reason = getattr(e, "reason", e)
            res.error_kind = type(reason).__name__ if not isinstance(reason, str) else "URLError"
            res.error = str(reason)[:300]
            # A TLS/SSL EOF on *every* host is an egress policy, not a data problem.
            if isinstance(reason, (ssl.SSLError,)) or "EOF occurred" in str(reason):
                res.error_kind = "EgressBlocked"
        except Exception as e:  # noqa: BLE001 - record, never crash the cycle
            res.error_kind = type(e).__name__
            res.error = str(e)[:300]
        res.elapsed_ms = int((time.monotonic() - t0) * 1000)
        if attempt < tries:
            time.sleep(config.HTTP_BACKOFF_SECONDS * attempt)
    return res


def utcnow_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
