"""Demo: load sample A-share daily bars offline and print a quick summary."""

from cnmarket import loader as L


def main():
    symbol = "600519"
    bars = L.load_daily(symbol, source="csv")  # offline, deterministic
    print(f"{symbol}: {len(bars)} daily bars (offline sample)")
    print("first:", bars[0])
    print("last :", bars[-1])
    closes = [b["close"] for b in bars]
    print(f"close range: {min(closes):.2f} – {max(closes):.2f}")
    print(f"latest close: {L.latest_close(bars)}")


if __name__ == "__main__":
    main()
