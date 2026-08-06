import time
import requests
from typing import Optional


class WebexClient:
    """Minimal sync Webex client for POC. Uses a BOT token passed at init.

    Methods return `requests.Response` objects.
    """

    def __init__(self, bot_token: str, base_url: str = "https://webexapis.com/v1", timeout: int = 15):
        self._bot_token = bot_token
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def _headers(self, extra: Optional[dict] = None):
        h = {"Authorization": f"Bearer {self._bot_token}", "Content-Type": "application/json"}
        if extra:
            h.update(extra)
        return h

    def _request(self, method: str, path: str, max_attempts: int = 3, backoff: float = 0.5, **kwargs) -> requests.Response:
        url = f"{self._base_url}{path}"
        last_exc = None
        for attempt in range(1, max_attempts + 1):
            try:
                resp = requests.request(method, url, headers=self._headers(kwargs.pop("headers", None)), timeout=self._timeout, **kwargs)
                # Do not automatically refresh token here; caller manages BOT token lifecycle.
                return resp
            except requests.RequestException as exc:
                last_exc = exc
                if attempt == max_attempts:
                    raise
                time.sleep(backoff * (2 ** (attempt - 1)))
        # unreachable
        raise last_exc

    def get(self, path: str, **kwargs) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._request("DELETE", path, **kwargs)
