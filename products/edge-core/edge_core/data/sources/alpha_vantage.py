import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

def get_alpha_vantage_daily_bars(ticker: str) -> pd.DataFrame:
    key = os.getenv('ALPHAVANTAGE_API_KEY') or os.getenv('ZE_ALPHA_VANTAGE_KEY')
    if not key:
        return pd.DataFrame()
    try:
        ts = TimeSeries(key=key)
        data, meta = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
        df = pd.DataFrame.from_dict(data, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.sort_index().reset_index().rename(columns={'index': 'date', '4. close': 'close'})
        return df[['date','close']]
    except Exception as e:
        print(f"WARN: Alpha Vantage daily failed: {e}")
        return pd.DataFrame()
