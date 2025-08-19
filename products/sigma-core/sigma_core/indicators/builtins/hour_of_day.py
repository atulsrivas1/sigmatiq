from ..base import Indicator
import pandas as pd


class HourOfDay(Indicator):
    NAME = "hour_of_day"
    CATEGORY = "time"
    SUBCATEGORY = "intraday"

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'hour_et' in df.columns:
            out['hour_of_day'] = pd.to_numeric(df['hour_et'], errors='coerce').astype(float)
            return out
        if 'date' in df.columns:
            out['hour_of_day'] = pd.to_datetime(df['date']).dt.tz_convert('US/Eastern').dt.hour.astype(float)
            return out
        out['hour_of_day'] = float('nan')
        return out

