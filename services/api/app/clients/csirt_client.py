from __future__ import annotations

import os
import time
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Optional

import requests


@dataclass(frozen=True)
class CSIRTSettings:
    base_url: str
    username: str
    password: str
    token_endpoint: str
    timeout: int
    verify_ssl: bool

    @staticmethod
    def from_env() -> "CSIRTSettings":
        base_url = os.getenv("CSIRT_BASE_URL", "").strip().rstrip("/")
        username = os.getenv("CSIRT_USERNAME", "").strip()
        password = os.getenv("CSIRT_PASSWORD", "").strip()

        token_endpoint = os.getenv("CSIRT_TOKEN_ENDPOINT", "/token").strip() or "/token"
        timeout = int((os.getenv("CSIRT_TIMEOUT", "30").strip() or "30"))

        verify_str = (os.getenv("CSIRT_VERIFY_SSL", "true") or "true").strip().lower()
        verify_ssl = verify_str in {"1", "true", "yes", "y", "on"}

        if not base_url:
            raise RuntimeError("Missing CSIRT_BASE_URL")
        if not username or not password:
            raise RuntimeError("Missing CSIRT_USERNAME or CSIRT_PASSWORD")

        return CSIRTSettings(
            base_url=base_url,
            username=username,
            password=password,
            token_endpoint=token_endpoint,
            timeout=timeout,
            verify_ssl=verify_ssl,
        )


class CSIRTClient:
    """
    Client CSIRT:
    - Obtiene Bearer token con username/password (via token_endpoint)
    - Reutiliza Session
    - Cachea token ~55min (ajustable)
    """

    def __init__(self, s: CSIRTSettings):
        self._s = s
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        self._bearer: Optional[str] = None
        self._bearer_exp: float = 0.0

    def _url(self, path: str) -> str:
        p = path.strip()
        if not p.startswith("/"):
            p = "/" + p
        return f"{self._s.base_url}{p}"

    def _ensure_token(self) -> None:
        # Reutiliza token vigente
        if self._bearer and time.time() < self._bearer_exp:
            return

        payload = {"username": self._s.username, "password": self._s.password}
        resp = self._session.post(
            self._url(self._s.token_endpoint),
            json=payload,
            timeout=self._s.timeout,
            verify=self._s.verify_ssl,
        )

        # Si falla, queremos ver el body para debug
        if resp.status_code >= 400:
            raise requests.HTTPError(
                f"{resp.status_code} {resp.reason} for url: {resp.url} | upstream_body={resp.text}",
                response=resp,
            )

        data = resp.json()
        access_token = data.get("access_token") or data.get("token")

        if not access_token:
            raise RuntimeError(f"Token response missing access_token/token: {data}")

        self._bearer = f"Bearer {access_token}"
        self._bearer_exp = time.time() + 55 * 60  # 55 min
        self._session.headers["Authorization"] = self._bearer

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        self._ensure_token()
        resp = self._session.get(
            self._url(path),
            params=params,
            timeout=self._s.timeout,
            verify=self._s.verify_ssl,
        )
        resp.raise_for_status()
        return resp.json()

    def post(self, path: str, json: dict[str, Any] | None = None) -> Any:
        self._ensure_token()
        resp = self._session.post(
            self._url(path),
            json=json,
            timeout=self._s.timeout,
            verify=self._s.verify_ssl,
        )
        resp.raise_for_status()
        return resp.json()


@lru_cache(maxsize=1)
def get_csirt_client() -> CSIRTClient:
    return CSIRTClient(CSIRTSettings.from_env())
