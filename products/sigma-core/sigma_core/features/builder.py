import numpy as np
import pandas as pd
import logging
from typing import List, Optional
from ..indicators.base import Indicator
from ..indicators.registry import get_indicator
from .sets import IndicatorSet


FEATURE_PREFIXES = [
    "calls_sold_d", "puts_sold_d",
    "close_mom_", "close_vol_",
    "bb_mid_", "bb_upper_", "bb_lower_",
    "macd_", "plus_di_", "minus_di_", "adx_",
    "atr_", "obv", "rsi_", "ema_", "dist_ema",
    "stoch_", "cci_", "williams_r_",
    "iv_",
]
FEATURE_COLUMNS_EXTRA = [
    "calls_sold_total",
    "puts_sold_total",
    "pc_ratio",
    "imbalance",
    "day_of_week",
    "hour_et",
    # Optional enhanced features if present
    "atm_calls",
    "atm_puts",
    "atm_pc_ratio",
    "atm_imbalance",
    # Daily and composite extras
    "vwap_d",
    "vwap_intraday",
    "momentum_score_total",
]

def select_features(df: pd.DataFrame) -> List[str]:
    cols = []
    for p in FEATURE_PREFIXES:
        cols.extend([c for c in df.columns if c.startswith(p)])
    cols.extend([c for c in FEATURE_COLUMNS_EXTRA if c in df.columns])
    return cols


class FeatureBuilder:
    def __init__(self, distance_max: int = 5, indicator_set: Optional[IndicatorSet] = None):
        self.distance_max = int(distance_max)
        self.indicator_set = indicator_set

    def add_base_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        # Per-distance features for calls/puts sold
        for d in range(-self.distance_max, self.distance_max + 1):
            df[f"calls_sold_d{d}"] = np.where(np.round(df["price_level"] - df["spy_prev_close"]) == d, df["calls_sold"], 0.0)
            df[f"puts_sold_d{d}"] = np.where(np.round(df["price_level"] - df["spy_prev_close"]) == d, df["puts_sold"], 0.0)
            if "calls_premium" in df.columns:
                df[f"calls_premium_d{d}"] = np.where(np.round(df["price_level"] - df["spy_prev_close"]) == d, df["calls_premium"], 0.0)
            if "puts_premium" in df.columns:
                df[f"puts_premium_d{d}"] = np.where(np.round(df["price_level"] - df["spy_prev_close"]) == d, df["puts_premium"], 0.0)
        # Totals and ratios
        df["calls_sold_total"] = df[[f"calls_sold_d{d}" for d in range(-self.distance_max, self.distance_max + 1)]].sum(axis=1)
        df["puts_sold_total"] = df[[f"puts_sold_d{d}" for d in range(-self.distance_max, self.distance_max + 1)]].sum(axis=1)
        df["pc_ratio"] = (df["puts_sold_total"] + 1e-6) / (df["calls_sold_total"] + 1e-6)
        df["imbalance"] = df["calls_sold_total"] - df["puts_sold_total"]
        # Premium totals if present
        prem_calls = [c for c in df.columns if c.startswith("calls_premium_d")]
        prem_puts = [c for c in df.columns if c.startswith("puts_premium_d")]
        if prem_calls:
            df["calls_premium_total"] = df[prem_calls].sum(axis=1)
        if prem_puts:
            df["puts_premium_total"] = df[prem_puts].sum(axis=1)
        # Inferred (trade-level) premium per-distance if present
        if "calls_premium_inf_sold" in df.columns or "puts_premium_inf_sold" in df.columns:
            for d in range(-self.distance_max, self.distance_max + 1):
                df[f"calls_premium_inf_sold_d{d}"] = np.where(df["price_level"] - df["spy_prev_close"] == d, df.get("calls_premium_inf_sold", 0.0), 0.0)
                df[f"puts_premium_inf_sold_d{d}"] = np.where(df["price_level"] - df["spy_prev_close"] == d, df.get("puts_premium_inf_sold", 0.0), 0.0)
        df["day_of_week"] = pd.to_datetime(df["date"]).dt.dayofweek
        return df

    def add_indicator_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        if self.indicator_set:
            for spec in self.indicator_set.indicators:
                try:
                    indicator_class = get_indicator(spec.name)
                    params = dict(spec.params or {})
                    indicator = indicator_class(**params)
                    df = pd.concat([df, indicator.calculate(df)], axis=1)
                except Exception:
                    # If indicator cannot be computed, skip gracefully but log
                    logging.getLogger(__name__).warning("indicator compute failed: %s", getattr(spec, 'name', 'unknown'))
        return df

    def add_dealer_orientation(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        if {"calls_sold_total", "puts_sold_total"}.issubset(df.columns):
            diff = df["puts_sold_total"].fillna(0.0) - df["calls_sold_total"].fillna(0.0)
            df["mm_profit_dir_simple"] = np.sign(diff).astype(float)
        else:
            df["mm_profit_dir_simple"] = 0.0
        return df

    def add_atm_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        try:
            anchor = np.round(df["spy_prev_close"].astype(float))
            is_atm = (df["price_level"].astype(float) == anchor)
            df["atm_calls"] = np.where(is_atm, df.get("calls_sold", 0.0), 0.0)
            df["atm_puts"] = np.where(is_atm, df.get("puts_sold", 0.0), 0.0)
            total = df["atm_calls"].fillna(0.0) + df["atm_puts"].fillna(0.0)
            df["atm_pc_ratio"] = (df["atm_puts"].fillna(0.0) + 1e-6) / (df["atm_calls"].fillna(0.0) + 1e-6)
            df["atm_imbalance"] = df["atm_calls"].fillna(0.0) - df["atm_puts"].fillna(0.0)
        except Exception:
            for c in ["atm_calls", "atm_puts", "atm_pc_ratio", "atm_imbalance"]:
                if c not in df.columns:
                    df[c] = 0.0
        return df
