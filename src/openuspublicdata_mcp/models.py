from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    official: bool
    jurisdiction: str
    auth: str
    licence: str | None = None
    platform: str = "direct_api"
    status: str = "active"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
