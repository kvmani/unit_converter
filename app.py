"""Compatibility launcher for source checkouts."""

from pathlib import Path
import sys

source_root = Path(__file__).resolve().parent / "src"
if str(source_root) not in sys.path:
    sys.path.insert(0, str(source_root))

from unit_converter_service.app import VERSION, app, main  # noqa: E402

__all__ = ["VERSION", "app", "main"]


if __name__ == "__main__":
    main()
