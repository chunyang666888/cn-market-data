"""cn-market-data — A-share daily-bar loader with an offline fallback.

``akshare`` is an *optional* dependency. When it is not installed (or the
network is unavailable), the loader falls back to the bundled sample CSV so the
library — and its tests — run fully offline.
"""

from .loader import load_daily, load_from_csv

__all__ = ["load_daily", "load_from_csv"]
