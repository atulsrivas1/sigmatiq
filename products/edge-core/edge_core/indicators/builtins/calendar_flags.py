from ..base import Indicator
import pandas as pd
import numpy as np


class CalendarFlags(Indicator):
    NAME = "calendar_flags"
    CATEGORY = "time"
    SUBCATEGORY = "calendar"

    def __init__(self, tz: str = 'US/Eastern'):
        self.tz = tz

    def _is_eom(self, d: pd.Timestamp) -> bool:
        return (d + pd.offsets.MonthEnd(0)).date() == d.date()

    def _is_eoq(self, d: pd.Timestamp) -> bool:
        return self._is_eom(d) and d.month in (3,6,9,12)

    def _is_opex(self, d: pd.Timestamp) -> bool:
        # Third Friday of the month
        if d.weekday() != 4:
            return False
        first = d.replace(day=1)
        first_friday = first + pd.offsets.Week(weekday=4)  # first Friday
        # third Friday = first Friday + 2 weeks
        third_friday = first_friday + pd.offsets.Week(2)
        return d.date() == third_friday.date()

    def _is_holiday_eve_simple(self, d: pd.Timestamp) -> bool:
        # Heuristic: day before New Year (1/1), Independence Day (7/4), Christmas (12/25)
        next_day = d + pd.Timedelta(days=1)
        mmdd = (next_day.month, next_day.day)
        return mmdd in {(1,1),(7,4),(12,25)}

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            for c in ('is_eom','is_eoq','is_opex','is_holiday_eve'):
                out[c] = float('nan')
            return out
        dt = pd.to_datetime(df['date']).dt.tz_convert(self.tz)
        days = dt.dt.normalize()
        uniq = days.drop_duplicates().reset_index(drop=True)
        flags = {}
        for t in uniq:
            ts = pd.Timestamp(t).tz_convert(self.tz)
            flags[ts] = {
                'is_eom': float(self._is_eom(ts)),
                'is_eoq': float(self._is_eoq(ts)),
                'is_opex': float(self._is_opex(ts)),
                'is_holiday_eve': float(self._is_holiday_eve_simple(ts)),
            }
        eom = []
        eoq = []
        opex = []
        hev = []
        for t in days:
            f = flags.get(pd.Timestamp(t).tz_convert(self.tz), {'is_eom':np.nan,'is_eoq':np.nan,'is_opex':np.nan,'is_holiday_eve':np.nan})
            eom.append(f['is_eom']); eoq.append(f['is_eoq']); opex.append(f['is_opex']); hev.append(f['is_holiday_eve'])
        out['is_eom'] = eom
        out['is_eoq'] = eoq
        out['is_opex'] = opex
        out['is_holiday_eve'] = hev
        return out

