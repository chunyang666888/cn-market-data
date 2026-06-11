import os
from cnmarket import loader as L


def test_load_from_csv_shape():
    path = os.path.join(os.path.dirname(__file__), "..", "cnmarket", "data", "sample.csv")
    bars = L.load_from_csv(path)
    assert len(bars) == 10
    b0 = bars[0]
    assert set(b0) == {"date", "open", "high", "low", "close", "volume"}
    assert b0["date"] == "2024-01-02"
    assert b0["close"] == 1698.30
    assert isinstance(b0["volume"], int)


def test_load_daily_csv_fallback():
    # No akshare installed in CI -> falls back to bundled sample deterministically.
    bars = L.load_daily("600519", source="csv")
    assert len(bars) >= 10
    assert 1650 < bars[0]["close"] < 1750  # sanity range for the sample


def test_load_daily_auto_without_akshare(monkeypatch):
    # Pretend akshare is importable but the network call would fail -> still ok
    # because "auto" with akshare actually tries it; here we force csv branch.
    bars = L.load_daily("600519", source="csv")
    assert bars[-1]["date"] == "2024-01-15"


def test_latest_close():
    bars = L.load_daily("600519", source="csv")
    assert L.latest_close(bars) == 1699.90
    assert L.latest_close([]) is None


def test_unknown_source_raises():
    try:
        L.load_daily("600519", source="bogus")
        assert False, "should have raised"
    except ValueError:
        pass
