# cn-market-data

A tiny, dependency-free loader for **A-share daily bars**. It tries
[`akshare`](https://akshare.akfamily.xyz/) for live data, but **falls back to a
bundled sample CSV** when akshare is absent or the network is down — so the
library and its tests always run offline and deterministically.

[![CI](https://github.com/chunyang666888/cn-market-data/actions/workflows/ci.yml/badge.svg)](https://github.com/chunyang666888/cn-market-data/actions)

```
pip install pytest
pytest -q
python examples/demo.py
```

## Usage

```python
from cnmarket import load_daily

# Offline, deterministic — reads the bundled sample (no akshare needed).
bars = load_daily("600519", source="csv")
print(bars[-1])   # {'date': '2024-01-15', 'open': ..., 'high': ..., ...}

# Live data (needs: pip install akshare, and network)
bars = load_daily("600519", source="akshare")

# "auto" (default): akshare if importable, else the bundled sample.
bars = load_daily("600519")
```

Each bar is a plain dict: `date, open, high, low, close, volume`.

## Why this repo

Most quant tutorials hard-depend on a data vendor and break the moment the API
changes or you are offline. This loader is the opposite: a clean, tested seam
between "I have a CSV" and "I have a live feed", so the rest of a strategy can
be built and tested without network access.

## License

MIT
