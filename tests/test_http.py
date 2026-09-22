"""HTTP integrity, strict parsing, response caps, and operator pacing."""
from __future__ import annotations

import io
import unittest
import urllib.error
from unittest import mock

from msl import http
from msl.http import FetchResult


class _Response:
    def __init__(self, body: bytes, status: int = 200,
                 content_type: str = "application/json"):
        self._body = body
        self.status = status
        self.headers = {"Content-Type": content_type}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, limit: int) -> bytes:
        return self._body[:limit]

    def geturl(self) -> str:
        return "https://example.test/final"


class StrictResponseHandling(unittest.TestCase):
    def test_json_rejects_nan_and_infinity(self):
        for token in (b"NaN", b"Infinity", b"-Infinity"):
            with self.assertRaises(ValueError):
                FetchResult(url="x", status=200,
                            body=b'{"value":' + token + b"}").json()

    def test_oversized_response_is_truncated_and_never_ok(self):
        response = _Response(b"123456")
        with mock.patch("urllib.request.urlopen", return_value=response):
            result = http.fetch("https://example.test/start", max_bytes=5, retries=1)
        self.assertTrue(result.truncated)
        self.assertFalse(result.ok)
        self.assertEqual(result.body, b"12345")
        self.assertEqual(result.error_kind, "ResponseTooLarge")
        self.assertEqual(result.final_url, "https://example.test/final")
        self.assertEqual(result.content_type, "application/json")

    def test_complete_response_keeps_exact_adapter_bytes(self):
        body = b'{"value":7}'
        with mock.patch("urllib.request.urlopen", return_value=_Response(body)):
            result = http.fetch("https://example.test/start", max_bytes=100, retries=1)
        self.assertTrue(result.ok)
        self.assertEqual(result.body, body)
        self.assertEqual(result.size, len(body))
        self.assertEqual(len(result.sha256), 64)

    def test_http_4xx_is_not_hammered_with_retries(self):
        error = urllib.error.HTTPError(
            "https://example.test/start", 429, "Too Many Requests", {},
            io.BytesIO(b'{"error":"slow down"}'))
        with mock.patch("urllib.request.urlopen", side_effect=error) as open_url, \
             mock.patch.object(http.time, "sleep") as sleep:
            result = http.fetch("https://example.test/start", retries=3)
        self.assertEqual(result.status, 429)
        self.assertEqual(result.attempts, 1)
        self.assertTrue(result.rate_limited)
        open_url.assert_called_once()
        sleep.assert_not_called()

    def test_plain_403_is_forbidden_not_automatically_rate_limited(self):
        error = urllib.error.HTTPError(
            "https://example.test/start", 403, "Forbidden", {},
            io.BytesIO(b"forbidden"))
        with mock.patch("urllib.request.urlopen", side_effect=error):
            result = http.fetch("https://example.test/start", retries=3)
        self.assertEqual(result.attempts, 1)
        self.assertFalse(result.rate_limited)


class HostPacing(unittest.TestCase):
    def setUp(self):
        http._LAST_REQUEST_BY_HOST.clear()

    def test_arxiv_calls_are_separated_by_three_seconds(self):
        with mock.patch.object(http.time, "monotonic",
                               side_effect=[100.0, 100.0, 101.0, 103.0]), \
             mock.patch.object(http.time, "sleep") as sleep:
            http._pace("https://export.arxiv.org/api/query?a=1")
            http._pace("https://export.arxiv.org/api/query?a=2")
        sleep.assert_called_once_with(2.0)

    def test_unclassified_hosts_are_not_delayed(self):
        with mock.patch.object(http.time, "sleep") as sleep:
            http._pace("https://example.test/data")
        sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main()
