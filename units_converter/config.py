"""Configuration settings for the units_converter package."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration with safe defaults for the API and batch tooling."""

    api_prefix: str = "/api/v1/units"
    max_upload_bytes: int = 5 * 1024 * 1024  # 5 MB
    max_rows: int = 10_000
    dev_port: int = 5007
    static_dir: Path = Path(__file__).resolve().parent / "ui_dev"


config = AppConfig()
