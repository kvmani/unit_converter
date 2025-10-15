"""Pydantic schemas for request validation."""
from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel, Field, validator


class ConvertRequest(BaseModel):
    value: float | str
    from_unit: str = Field(alias="from")
    to_unit: str = Field(alias="to")
    mode: str = "absolute"
    sig_figs: Optional[int] = None
    decimals: Optional[int] = None
    notation: str = "auto"

    class Config:
        allow_population_by_field_name = True
        allow_population_by_alias = True

    @validator("mode")
    def validate_mode(cls, value: str) -> str:
        if value not in {"absolute", "interval"}:
            raise ValueError("mode must be 'absolute' or 'interval'")
        return value

    @validator("notation")
    def validate_notation(cls, value: str) -> str:
        if value not in {"auto", "engineering", "scientific"}:
            raise ValueError("notation must be auto, engineering, or scientific")
        return value

    @validator("sig_figs")
    def validate_sig_figs(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value <= 0:
            raise ValueError("sig_figs must be positive")
        return value

    @validator("decimals")
    def validate_decimals(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value < 0:
            raise ValueError("decimals must be non-negative")
        return value


class ExpressionRequest(BaseModel):
    expression: str


class BatchOptionsModel(BaseModel):
    targets: Dict[str, str] = Field(default_factory=dict)
    mode: Dict[str, str] = Field(default_factory=dict)

    @validator("mode", each_item=True)
    def validate_mode_entries(cls, value: str) -> str:
        if value not in {"absolute", "interval"}:
            raise ValueError("mode overrides must be 'absolute' or 'interval'")
        return value
