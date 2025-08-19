import numpy as np
import pandas as pd


def label_next_hour_direction(df_hourly: pd.DataFrame, *, k_sigma: float = 0.3, fixed_bp: float | None = None) -> pd.DataFrame:
    """
    Label next-hour direction with an optional flat band determined by k_sigma * std.
    Produces columns y (UP/DOWN/FLAT) and y_syn (synthetic fallback if y missing).
    """
    df = df_hourly.copy()
    df = df.sort_values(["date", "hour_et"]) if {"date","hour_et"}.issubset(df.columns) else df.copy()
    close = df["close"].astype(float).values
    ret = np.zeros_like(close)
    ret[:-1] = (close[1:] - close[:-1]) / (close[:-1] + 1e-12)
    ret[-1] = 0.0
    df["ret_next_hour"] = pd.Series(ret, index=df.index)

    if fixed_bp is not None:
        thr = float(fixed_bp) / 10000.0
    else:
        std = float(np.nanstd(ret))
        thr = k_sigma * std
    y = np.where(ret > thr, "UP", np.where(ret < -thr, "DOWN", "FLAT"))
    df["y_syn"] = y
    # If real labels column exists, preserve it as y; otherwise use y_syn
    if "y" not in df.columns:
        df["y"] = df["y_syn"]
    return df
