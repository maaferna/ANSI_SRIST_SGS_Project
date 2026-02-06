from __future__ import annotations

from typing import Any, List, Optional, Union

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, ConfigDict

from app.clients.csirt_client import get_csirt_client

router = APIRouter(prefix="/csirt", tags=["csirt"])


class AptCatQuery(BaseModel):
    """
    Matches CSIRT OpenAPI schema: AptCatQuery

    Fields are optional and allow either:
      - string
      - list[string]
      - null
    """
    model_config = ConfigDict(extra="forbid")

    ttp: Optional[Union[str, List[str]]] = Field(default=None, description="TTP or list of TTPs")
    apt: Optional[Union[str, List[str]]] = Field(default=None, description="APT or list of APTs")
    categoria_malware: Optional[Union[str, List[str]]] = Field(
        default=None,
        description=(
            "Malware category or list of categories. "
            "Examples: ransomware, spyware, trojan, worm, botnet, rat, etc."
        ),
    )


@router.post("/malware/info")
def malware_info(payload: AptCatQuery) -> dict[str, Any]:
    """
    Proxy to CSIRT: POST /malware/info

    CSIRT expects JSON body like:
      {"categoria_malware": "ransomware"}
    or:
      {"categoria_malware": ["ransomware", "spyware"]}

    Returns the upstream JSON response as-is under 'data'.
    """
    client = get_csirt_client()
    upstream_path = "/malware/info"

    try:
        data = client.post(upstream_path, json=payload.model_dump(exclude_none=True))
        return {"ok": True, "endpoint": upstream_path, "data": data}
    except Exception as e:
        # If your client wraps requests.HTTPError, you'll get useful text here.
        raise HTTPException(status_code=502, detail=f"CSIRT request failed: {e}")


@router.get("/health")
def csirt_health() -> dict[str, Any]:
    """
    Liveness check for your FastAPI service (not the CSIRT upstream).
    Use this to confirm the route is reachable through Nginx.
    """
    return {"ok": True, "service": "api", "router": "csirt"}
