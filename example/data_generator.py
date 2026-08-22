"""Random walk data for the examples.

Times are `YYYY-MM-DD` strings, which lightweight-charts reads as business days.
Callback payloads report times back in the same form they were given in, so a
series built from strings reports strings.
"""
import random
from datetime import date, timedelta


def _dates(t0, n):
    start = date.fromisoformat(t0)
    return [(start + timedelta(days=i)).isoformat() for i in range(n)]


def generate_random_ohlc(v0, ret=0.05, n=500, t0='2021-01-01'):
    """Candlestick and bar data: time, open, high, low, close."""
    out, close = [], v0
    for t in _dates(t0, n):
        o = close
        close = o * (1 + random.uniform(-ret, ret))
        out.append({
            'time': t,
            'open': o,
            'high': max(o, close) * (1 + random.uniform(0, ret)),
            'low': min(o, close) * (1 + random.uniform(-ret, 0)),
            'close': close,
        })
    return out


def generate_random_series(v0, ret=0.05, n=500, t0='2021-01-01'):
    """Single-value data for line, area, baseline and histogram series."""
    out, value = [], v0
    for t in _dates(t0, n):
        value = value * (1 + random.uniform(-ret, ret))
        out.append({'time': t, 'value': value})
    return out
