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
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from . import config


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

    @property
    def ok(self) -> bool:
        return self.status is not None and 200 <= self.status < 300

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.body).hexdigest()

    @property
    def size(self) -> int:
        return len(self.body)

    def text(self) -> str:
        return self.body.decode("utf-8", "replace")

    def json(self) -> Any:
        """Parse the body, or raise.  Callers must treat a raise as a failed read."""
        return json.loads(self.text())

    def describe_error(self) -> str:
        return f"{self.error_kind or 'unknown'}: {self.error or ''}".strip()


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
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout or config.HTTP_TIMEOUT,
                                        context=ctx) as r:
                raw = r.read(limit + 1)
                res.status = r.status
                res.content_type = r.headers.get("Content-Type") or ""
                res.final_url = r.geturl() or url
                res.body = _decompress(r, raw)[:limit]
                res.elapsed_ms = int((time.monotonic() - t0) * 1000)
                res.error = None
                res.error_kind = None
                return res
        except urllib.error.HTTPError as e:
            res.status = e.code
            res.error_kind = "HTTPError"
            res.error = f"HTTP {e.code} {e.reason}"
            # 403/429 from GitHub mean "rate limited", not "broken"; do not hammer.
            res.rate_limited = e.code in (403, 429)
            try:
                res.body = e.read(limit)[:limit]
            except Exception:
                res.body = b""
            res.content_type = (e.headers or {}).get("Content-Type") or ""
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
