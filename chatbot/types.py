"""
Lightweight protocols and shared types to help static checking.
"""

from typing import Any, Protocol


class Chain(Protocol):
    def invoke(self, inputs: dict[str, Any]) -> str: ...
