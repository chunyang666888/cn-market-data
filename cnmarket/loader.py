"""A-share daily-bar loading.

Public API
----------
``load_daily(symbol, source="auto")``
    Return a list of daily bars (dicts) for ``symbol`` (e.g. ``"600519"``).
    With ``source="akshare"`` it uses the optional ``akshare`` package; with
    ``source="csv"`` (or automatically when akshare is missing) it reads the
    bundled sample so everything is reproducible offline.

``load_from_csv(path)``
    Parse a CSV with columns date,open,high,low,close,volume into bars.
"""

import csv
import os
from datetime import date

_HERE = os.path.dirname(__file__)
_SAMPLE_DIR = os.path.join(_HERE, "data")


def _bar(row):
    return {
        "date": row["date"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(float(row["volume"])),
    }


def load_from_csv(path):
    """Read an OHLCV csv (header required) into a list of bar dicts."""
    bars = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            bars.append(_bar(row))
    return bars


def _sample_path(symbol):
    # Look for data/<symbol>.csv, else the generic sample.
    cand = os.path.join(_SAMPLE_DIR, f"{symbol}.csv")
    if os.path.exists(cand):
        return cand
    return os.path.join(_SAMPLE_DIR, "sample.csv")


def load_daily(symbol, source="auto"):
    """Load daily bars for an A-share ``symbol``.

    source:
      "csv"     -> always use the bundled sample (offline, deterministic)
      "akshare" -> use the optional akshare package (needs network + install)
      "auto"    -> akshare if importable, else bundled sample (default)
    """
    if source == "csv":
        return load_from_csv(_sample_path(symbol))

    if source in ("auto", "akshare"):
        try:
            import akshare as ak  # type: ignore
        except ImportError:
            if source == "akshare":
                raise RuntimeError("akshare not installed: pip install akshare")
            return load_from_csv(_sample_path(symbol))
        # akshare path (only reached if akshare is importable and source!=csv)
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily",
                                adjust="qfq")
        bars = []
        for _, r in df.iterrows():
            bars.append({
                "date": str(r["日期"]),
                "open": float(r["开盘"]),
                "high": float(r["最高"]),
                "low": float(r["最低"]),
                "close": float(r["收盘"]),
                "volume": int(float(r["成交量"])),
            })
        return bars
    raise ValueError("source must be 'auto', 'csv' or 'akshare'")


def latest_close(bars):
    """Convenience: most-recent close (bars assumed chronological)."""
    return bars[-1]["close"] if bars else None
