from dataclasses import dataclass, field
from typing import Any


@dataclass
class Response:
    data: Any
    detail: str
    message: str
    status: int = 0
