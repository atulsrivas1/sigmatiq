from .sources.polygon import get_polygon_hourly_bars, get_polygon_daily_bars
import pandas as pd

def get_multi_timeframe_data(ticker: str, start_date: str, end_date: str, intervals: list[str]) -> dict[str, pd.DataFrame]:
    out: dict[str, pd.DataFrame] = {}
    if 'hour' in intervals:
        out['hour'] = get_polygon_hourly_bars(ticker, start_date, end_date)
    if 'day' in intervals:
        out['day'] = get_polygon_daily_bars(ticker, start_date, end_date)
    return out
