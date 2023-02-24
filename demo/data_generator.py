import random

import pandas as pd

def generate_random_series(*args, **kwargs):
    return generate_random_ohlc(*args, **kwargs, close_only=True)

def generate_random_ohlc(v0: float, ret=0.05, n=500, t0='2021-01-01', close_only=False):
    datelist = [dt.strftime('%Y-%m-%d') for dt in pd.date_range(t0, periods=n).tolist()]
    res = []
    c = v0
    for dt in datelist:
        o = c
        c = o * (1 + random.uniform(-ret, ret))
        if not close_only:
            h = max(o, c) * (1 + random.uniform(0, ret))
            l = min(o, c) * (1 + random.uniform(-ret, 0))
            res.append({
                "time": dt,
                "open": o,
                "high": h,
                "low": l,
                "close": c
            })
        else:
            res.append({
                "time": dt,
                "value": c
            })
        o = c
    return res
