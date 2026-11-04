"""Fail-closed stdlib client for the verified Marketing AI shortform provider."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class MarketingShortformClientError(RuntimeError):
    pass


class MarketingAuthRequired(MarketingShortformClientError):
    pass


@dataclass(frozen=True)
class MarketingShortformClient:
    base_url: str = "http://127.0.0.1:4318"
    contract_path: str = "/v1/shortform/contracts"
    approved_contract_path: str = "/v1/shortform/e2e/approved-contract"
    timeout_seconds: float = 8.0

    @classmethod
    def from_env(cls) -> "MarketingShortformClient":
        return cls(
            base_url=os.environ.get("MARKETING_SHORTFORM_BASE_URL", cls.base_url).rstrip("/"),
            contract_path=os.environ.get("MARKETING_SHORTFORM_CONTRACT_PATH", cls.contract_path),
            approved_contract_path=os.environ.get("MARKETING_SHORTFORM_E2E_CONTRACT_PATH", cls.approved_contract_path),
        )

    def _token(self) -> str:
        token = os.environ.get("MARKETING_SHORTFORM_BRIDGE_TOKEN", "").strip()
        if not token:
            raise MarketingAuthRequired("MARKETING_SHORTFORM_BRIDGE_TOKEN is required")
        return token

    def _request(self, method: str, path: str, payload: dict | None = None) -> dict:
        token = self._token()
        body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = Request(f"{self.base_url}{path}", data=body, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            raise MarketingShortformClientError(f"Marketing provider returned HTTP {error.code}") from error
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            raise MarketingShortformClientError("Marketing provider is unreachable or returned invalid JSON") from error

    def create_contract(self, payload: dict) -> dict:
        return self._request("POST", self.contract_path, payload)

    def approved_contract(self) -> dict:
        return self._request("GET", self.approved_contract_path)
