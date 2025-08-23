import os
import pandas as pd
from dotenv import load_dotenv
from datetime import date, timedelta, datetime
import json
import time
import numpy as np
import requests
import pytz

CACHE_DIR = "data_cache"
VERBOSE = os.getenv("POLYGON_VERBOSE", "0") in ("1", "true", "True")

def _today_et() -> date:
    eastern = pytz.timezone('US/Eastern')
    return datetime.now(eastern).date()

def get_polygon_options_aggs(
    underlying_ticker: str,
    expiration_date: date,
    strike_price: float,
    option_type: str,
    from_date: date,
    to_date: date,
    *,
    timeout_seconds: int = 10,
    retries: int = 3,
) -> pd.DataFrame:
    """
    Fetches 1-minute aggregate bars for a specific option contract from Polygon.io and uses a file-based cache.

    Args:
        underlying_ticker (str): The underlying stock ticker (e.g., SPY).
        expiration_date (date): The expiration date of the option.
        strike_price (float): The strike price of the option.
        option_type (str): 'call' or 'put'.
        from_date (date): The start date for the aggregates.
        to_date (date): The end date for the aggregates.

    Returns:
        pd.DataFrame: DataFrame containing the 1-minute OHLCV data for the option.
    """
    # Construct OCC symbol
    expiration_date_str = expiration_date.strftime("%y%m%d")
    option_type_char = 'C' if option_type == "call" else 'P'
    strike_price_cents = int(strike_price * 1000)
    strike_price_cents_str = f"{strike_price_cents:08d}"
    ticker = f"O:{underlying_ticker}{expiration_date_str}{option_type_char}{strike_price_cents_str}"

    os.makedirs(CACHE_DIR, exist_ok=True)
    is_today = (from_date == _today_et()) or (to_date == _today_et())
    cache_key = f"{ticker.replace(':', '_')}_{from_date.strftime('%Y-%m-%d')}"
    cache_file_path = os.path.join(CACHE_DIR, f"{cache_key}.json")

    if (not is_today) and os.path.exists(cache_file_path):
        try:
            with open(cache_file_path, 'r') as f:
                if os.fstat(f.fileno()).st_size < 5:
                    os.remove(cache_file_path)
                else:
                    data_json = json.load(f)
                    df = pd.DataFrame(data_json)
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    return df
        except json.JSONDecodeError:
            try:
                os.remove(cache_file_path)
            except Exception:
                pass

    print(f"Fetching options aggregates for {ticker} from Polygon.io API...")
    # Support ZE_POLYGON_API_KEY fallback for compatibility
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY") or os.getenv("ZE_POLYGON_API_KEY")
    if not POLYGON_API_KEY:
        raise ValueError("POLYGON_API_KEY (or ZE_POLYGON_API_KEY) environment variable not set.")

    try:
        # Construct the API URL for aggregates
        api_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{from_date.strftime('%Y-%m-%d')}/{to_date.strftime('%Y-%m-%d')}"
        print(f"Requesting Polygon API: {api_url}")  # Added for debugging

        params = {
            "adjusted": "false",
            "sort": "asc",
            "limit": 50000,
            "apiKey": POLYGON_API_KEY,
        }

        last_err = None
        for attempt in range(1, retries + 1):
            try:
                if VERBOSE:
                    print(f"Polygon GET {api_url} attempt {attempt}/{retries} (from={from_date}, to={to_date})")
                response = requests.get(api_url, params=params, timeout=timeout_seconds)
                response.raise_for_status()  # Raise an exception for HTTP errors
                data = response.json()
                if VERBOSE:
                    try:
                        res_len = len(data.get('results', []))
                    except Exception:
                        res_len = 'unknown'
                    print(f"Options aggs status={response.status_code} results={res_len}")
                break
            except requests.exceptions.RequestException as e:
                last_err = e
                print(f"WARNING: Options agg request failed for {ticker} (attempt {attempt}/{retries}): {e}")
                # Exponential backoff: 1s, 2s, 4s ...
                time.sleep(2 ** (attempt - 1))
        else:
            raise last_err

        if not data or not data.get('results'):
            print(f"No options aggregates found for {ticker}.")
            # Do not write an empty cache file, so we can retry later
            return pd.DataFrame()

        all_options_data = []
        eastern = pytz.timezone('US/Eastern')

        for result in data['results']:
            timestamp = datetime.fromtimestamp(result['t'] / 1000.0, tz=pytz.utc)
            timestamp_eastern = timestamp.astimezone(eastern)
            open_price = result.get('o', 0)
            high_price = result.get('h', 0)
            low_price = result.get('l', 0)
            close_price = result.get('c', 0)
            volume = result.get('v', 0)
            vwap = result.get('vw', None)
            all_options_data.append({
                'timestamp': timestamp_eastern,
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': volume,
                'vwap': vwap,
            })

        df = pd.DataFrame(all_options_data)
        # Only write to cache if we actually got some data
        if (not is_today) and (not df.empty):
            try:
                with open(cache_file_path, 'w') as f:
                    json.dump(df.to_dict(orient='records'), f, default=str)
            except Exception:
                pass
        return df
    except Exception as e:
        print(f"Error fetching options aggregates for {ticker}: {e}")
        return pd.DataFrame()

def _build_occ_symbol(underlying_ticker: str, expiration_date: date, strike_price: float, option_type: str) -> str:
    expiration_date_str = expiration_date.strftime("%y%m%d")
    option_type_char = 'C' if option_type == "call" else 'P'
    strike_price_cents = int(strike_price * 1000)
    strike_price_cents_str = f"{strike_price_cents:08d}"
    return f"O:{underlying_ticker}{expiration_date_str}{option_type_char}{strike_price_cents_str}"

def get_polygon_option_trades(
    underlying_ticker: str,
    expiration_date: date,
    strike_price: float,
    option_type: str,
    from_date: date,
    to_date: date,
    *,
    timeout_seconds: int = 15,
    retries: int = 3,
):
    """Fetch option trades (v3) for an OCC symbol; returns DataFrame with ts, price, size, conditions.
    Uses file cache under data_cache/trades/.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    occ = _build_occ_symbol(underlying_ticker, expiration_date, strike_price, option_type)
    cache_dir = os.path.join(CACHE_DIR, "trades")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file_path = os.path.join(cache_dir, f"{occ.replace(':','_')}_{from_date}_{to_date}.json")

    is_today = (from_date == _today_et()) or (to_date == _today_et())
    if (not is_today) and os.path.exists(cache_file_path):
        try:
            with open(cache_file_path, 'r') as f:
                data_json = json.load(f)
            df = pd.DataFrame(data_json)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception:
            pass

    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY") or os.getenv("ZE_POLYGON_API_KEY")
    if not POLYGON_API_KEY:
        return pd.DataFrame()
    base = f"https://api.polygon.io/v3/trades/options/{occ}"
    params = {
        "limit": 50000,
        "sort": "asc",
        "timestamp.gte": from_date.strftime("%Y-%m-%dT09:30:00Z"),
        "timestamp.lte": to_date.strftime("%Y-%m-%dT20:00:00Z"),
        "apiKey": POLYGON_API_KEY,
    }
    eastern = pytz.timezone('US/Eastern')
    results = []
    cursor = None
    for attempt in range(1, retries + 1):
        try:
            while True:
                q = params.copy()
                if cursor:
                    q['cursor'] = cursor
                r = requests.get(base, params=q, timeout=timeout_seconds)
                r.raise_for_status()
                data = r.json() or {}
                res = data.get('results') or []
                for tr in res:
                    ts = datetime.fromtimestamp(tr.get('t', 0)/1000000000.0, tz=pytz.utc) if 't' in tr else None
                    if ts is None:
                        continue
                    results.append({
                        'timestamp': ts.astimezone(eastern),
                        'price': tr.get('p', 0.0),
                        'size': tr.get('s', 0.0),
                        'conditions': tr.get('conditions', []),
                    })
                cursor = data.get('next_url') or data.get('next_page_token')
                if not cursor:
                    break
            break
        except Exception as e:
            if attempt == retries:
                print(f"WARN: trades fetch failed for {occ}: {e}")
                break
            time.sleep(2 ** (attempt - 1))
    df = pd.DataFrame(results)
    if not is_today:
        try:
            with open(cache_file_path, 'w') as f:
                json.dump(df.to_dict(orient='records'), f, default=str)
        except Exception:
            pass
    return df

def get_polygon_option_quotes(
    underlying_ticker: str,
    expiration_date: date,
    strike_price: float,
    option_type: str,
    from_date: date,
    to_date: date,
    *,
    timeout_seconds: int = 15,
    retries: int = 3,
):
    """Fetch option quotes (v3) for an OCC symbol; returns DataFrame with ts, bid, ask. Cached under data_cache/quotes/.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    occ = _build_occ_symbol(underlying_ticker, expiration_date, strike_price, option_type)
    cache_dir = os.path.join(CACHE_DIR, "quotes")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file_path = os.path.join(cache_dir, f"{occ.replace(':','_')}_{from_date}_{to_date}.json")

    is_today = (from_date == _today_et()) or (to_date == _today_et())
    if (not is_today) and os.path.exists(cache_file_path):
        try:
            with open(cache_file_path, 'r') as f:
                data_json = json.load(f)
            df = pd.DataFrame(data_json)
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception:
            pass

    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY") or os.getenv("ZE_POLYGON_API_KEY")
    if not POLYGON_API_KEY:
        return pd.DataFrame()
    base = f"https://api.polygon.io/v3/quotes/options/{occ}"
    params = {
        "limit": 50000,
        "sort": "asc",
        "timestamp.gte": from_date.strftime("%Y-%m-%dT09:30:00Z"),
        "timestamp.lte": to_date.strftime("%Y-%m-%dT20:00:00Z"),
        "apiKey": POLYGON_API_KEY,
    }
    eastern = pytz.timezone('US/Eastern')
    results = []
    cursor = None
    for attempt in range(1, retries + 1):
        try:
            while True:
                q = params.copy()
                if cursor:
                    q['cursor'] = cursor
                r = requests.get(base, params=q, timeout=timeout_seconds)
                r.raise_for_status()
                data = r.json() or {}
                res = data.get('results') or []
                for qt in res:
                    ts = datetime.fromtimestamp(qt.get('t', 0)/1000000000.0, tz=pytz.utc) if 't' in qt else None
                    if ts is None:
                        continue
                    results.append({
                        'timestamp': ts.astimezone(eastern),
                        'bid': qt.get('bp', None),
                        'ask': qt.get('ap', None),
                    })
                cursor = data.get('next_url') or data.get('next_page_token')
                if not cursor:
                    break
            break
        except Exception as e:
            if attempt == retries:
                print(f"WARN: quotes fetch failed for {occ}: {e}")
                break
            time.sleep(2 ** (attempt - 1))
    df = pd.DataFrame(results)
    if not is_today:
        try:
            with open(cache_file_path, 'w') as f:
                json.dump(df.to_dict(orient='records'), f, default=str)
        except Exception:
            pass
    return df

def get_polygon_option_chain_snapshot(
    underlying_ticker: str,
    expiration_date: date,
    *,
    timeout_seconds: int = 20,
    retries: int = 3,
) -> pd.DataFrame:
    """Fetch option chain snapshot for an underlying+expiry with Greeks and IV.
    Returns DataFrame with columns: strike, contract_type, implied_volatility, delta, gamma, theta, vega, bid, ask, mid, open_interest.
    Cached under data_cache/snapshot/.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_dir = os.path.join(CACHE_DIR, "snapshot")
    os.makedirs(cache_dir, exist_ok=True)
    key = f"{underlying_ticker}_{expiration_date.isoformat()}"
    cache_path = os.path.join(cache_dir, key + ".json")
    if (expiration_date != _today_et()) and os.path.exists(cache_path):
        try:
            with open(cache_path, 'r') as f:
                data_json = json.load(f)
            return pd.DataFrame(data_json)
        except Exception:
            pass

    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY") or os.getenv("ZE_POLYGON_API_KEY")
    if not POLYGON_API_KEY:
        return pd.DataFrame()
    base = f"https://api.polygon.io/v3/snapshot/options/{underlying_ticker}"
    params = {
        "expiration_date": expiration_date.strftime("%Y-%m-%d"),
        "limit": 1000,
        "apiKey": POLYGON_API_KEY,
    }
    results = []
    cursor = None
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            page_guard = 0
            while True:
                q = params.copy()
                if cursor:
                    q["cursor"] = cursor
                r = requests.get(base, params=q, timeout=timeout_seconds)
                r.raise_for_status()
                data = r.json() or {}
                res = data.get("results") or []
                for c in res:
                    strike = c.get("strike_price") or c.get("strike")
                    side = str(c.get("contract_type", "call")).lower()
                    details = c.get("details", {}) if isinstance(c.get("details", {}), dict) else {}
                    oi_val = c.get("open_interest", None)
                    if oi_val is None:
                        oi_val = details.get("open_interest", 0.0)
                    last_quote = c.get("last_quote", {}) if isinstance(c.get("last_quote", {}), dict) else {}
                    bid = last_quote.get("bid", last_quote.get("bp", None))
                    ask = last_quote.get("ask", last_quote.get("ap", None))
                    mid = None
                    try:
                        if bid is not None and ask is not None:
                            mid = 0.5 * (float(bid) + float(ask))
                    except Exception:
                        mid = None
                    greeks = c.get("greeks", {}) if isinstance(c.get("greeks", {}), dict) else {}
                    iv = c.get("implied_volatility", None)
                    results.append({
                        "strike": float(strike) if strike is not None else None,
                        "contract_type": side,
                        "implied_volatility": float(iv) if iv is not None else None,
                        "delta": greeks.get("delta", None),
                        "gamma": greeks.get("gamma", None),
                        "theta": greeks.get("theta", None),
                        "vega": greeks.get("vega", None),
                        "bid": bid,
                        "ask": ask,
                        "mid": mid,
                        "open_interest": float(oi_val or 0.0),
                    })
                cursor = data.get("next_page_token")
                page_guard += 1
                if not cursor or page_guard > 20:
                    break
            break
        except Exception as e:
            last_err = e
            time.sleep(2 ** (attempt - 1))
            continue
    df = pd.DataFrame(results)
    if expiration_date != _today_et():
        try:
            with open(cache_path, 'w') as f:
                json.dump(df.to_dict(orient='records'), f, default=str)
        except Exception:
            pass
    return df

def get_polygon_hourly_bars(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    # Use HTTP with API key; requests honors system proxy env vars if set
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY") or os.getenv("ZE_POLYGON_API_KEY")
    if not POLYGON_API_KEY:
        raise ValueError("POLYGON_API_KEY (or ZE_POLYGON_API_KEY) is not set.")
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/hour/{start_date}/{end_date}"
    params = {"adjusted": "false", "sort": "asc", "limit": 50000, "apiKey": POLYGON_API_KEY}
    # Cache historical (never today) to reduce load and allow offline reuse
    os.makedirs(CACHE_DIR, exist_ok=True)
    try:
        sd = datetime.strptime(start_date, "%Y-%m-%d").date()
        ed = datetime.strptime(end_date, "%Y-%m-%d").date()
    except Exception:
        sd = None; ed = None
    is_today = (sd == _today_et()) or (ed == _today_et()) if (sd and ed) else False
    cache_path = os.path.join(CACHE_DIR, f"{ticker}_hour_{start_date}_{end_date}.json")
    if (not is_today) and os.path.exists(cache_path):
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
            return pd.DataFrame(data)
        except Exception:
            try:
                os.remove(cache_path)
            except Exception:
                pass
    # Retry with exponential backoff
    last_err = None
    for attempt in range(1, 4):
        try:
            r = requests.get(url, params=params, timeout=20)
            r.raise_for_status()
            data = r.json() or {}
            results = data.get('results') or []
            if not results:
                return pd.DataFrame()
            rows = []
            for res in results:
                ts = datetime.fromtimestamp(res['t']/1000.0, tz=pytz.utc)
                rows.append({
                    'date': ts,
                    'open': res.get('o',0),
                    'high': res.get('h',0),
                    'low': res.get('l',0),
                    'close': res.get('c',0),
                    'volume': res.get('v',0),
                    'vwap': res.get('vw', None),
                })
            df = pd.DataFrame(rows)
            if (not is_today) and not df.empty:
                try:
                    with open(cache_path, 'w') as f:
                        json.dump(df.to_dict(orient='records'), f, default=str)
                except Exception:
                    pass
            return df
        except requests.exceptions.RequestException as e:
            last_err = e
            time.sleep(2 ** (attempt - 1))
    # If we get here, all attempts failed
    raise requests.exceptions.ConnectionError(f"Failed to fetch hourly bars from Polygon: {last_err}")

def get_polygon_daily_bars(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY") or os.getenv("ZE_POLYGON_API_KEY")
    if not POLYGON_API_KEY:
        raise ValueError("POLYGON_API_KEY (or ZE_POLYGON_API_KEY) is not set.")
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}"
    params = {"adjusted": "false", "sort": "asc", "limit": 50000, "apiKey": POLYGON_API_KEY}

    # Cache historical (never today) to reduce load and allow offline reuse
    os.makedirs(CACHE_DIR, exist_ok=True)
    try:
        sd = datetime.strptime(start_date, "%Y-%m-%d").date()
        ed = datetime.strptime(end_date, "%Y-%m-%d").date()
    except Exception:
        sd = None; ed = None
    is_today = (sd == _today_et()) or (ed == _today_et()) if (sd and ed) else False
    cache_path = os.path.join(CACHE_DIR, f"{ticker}_day_{start_date}_{end_date}.json")
    if (not is_today) and os.path.exists(cache_path):
        try:
            with open(cache_path, 'r') as f:
                data_cached = json.load(f)
            return pd.DataFrame(data_cached)
        except Exception:
            try:
                os.remove(cache_path)
            except Exception:
                pass

    last_err = None
    for attempt in range(1, 4):
        try:
            r = requests.get(url, params=params, timeout=20)
            r.raise_for_status()
            data = r.json()
            if not data or not data.get('results'):
                return pd.DataFrame()
            rows = []
            for res in data['results']:
                ts = datetime.fromtimestamp(res['t']/1000.0, tz=pytz.utc)
                rows.append({
                    'date': ts,
                    'open': res.get('o',0),
                    'high': res.get('h',0),
                    'low': res.get('l',0),
                    'close': res.get('c',0),
                    'volume': res.get('v',0),
                    'vwap': res.get('vw', None),
                })
            df = pd.DataFrame(rows)
            if (not is_today) and not df.empty:
                try:
                    with open(cache_path, 'w') as f:
                        json.dump(df.to_dict(orient='records'), f, default=str)
                except Exception:
                    pass
            return df
        except requests.exceptions.RequestException as e:
            last_err = e
            time.sleep(2 ** (attempt - 1))
    raise requests.exceptions.ConnectionError(f"Failed to fetch daily bars from Polygon: {last_err}")

def get_polygon_index_daily_bars(index_ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch daily bars for an index (e.g., I:VIX, I:VIX3M). Same shape as get_polygon_daily_bars.
    """
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY") or os.getenv("ZE_POLYGON_API_KEY")
    if not POLYGON_API_KEY:
        raise ValueError("POLYGON_API_KEY (or ZE_POLYGON_API_KEY) is not set.")
    url = f"https://api.polygon.io/v2/aggs/ticker/{index_ticker}/range/1/day/{start_date}/{end_date}"
    params = {"adjusted": "false", "sort": "asc", "limit": 50000, "apiKey": POLYGON_API_KEY}
    last_err = None
    for attempt in range(1, 4):
        try:
            r = requests.get(url, params=params, timeout=20)
            r.raise_for_status()
            data = r.json()
            if not data or not data.get('results'):
                return pd.DataFrame()
            rows = []
            for res in data['results']:
                ts = datetime.fromtimestamp(res['t']/1000.0, tz=pytz.utc)
                rows.append({
                    'date': ts,
                    'open': res.get('o',0),
                    'high': res.get('h',0),
                    'low': res.get('l',0),
                    'close': res.get('c',0),
                    'volume': res.get('v',0),
                    'vwap': res.get('vw', None),
                })
            return pd.DataFrame(rows)
        except requests.exceptions.RequestException as e:
            last_err = e
            time.sleep(2 ** (attempt - 1))
    raise requests.exceptions.ConnectionError(f"Failed to fetch daily bars from Polygon: {last_err}")

def get_polygon_agg_bars(ticker: str, multiplier: int, timespan: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Generic aggregates fetcher (e.g., 5-minute bars). Returns DataFrame with 'date' ts and OHLCV/VWAP.
    Historical ranges are cached on disk; today's data is never cached.
    """
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY") or os.getenv("ZE_POLYGON_API_KEY")
    if not POLYGON_API_KEY:
        raise ValueError("POLYGON_API_KEY (or ZE_POLYGON_API_KEY) is not set.")
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{int(multiplier)}/{timespan}/{start_date}/{end_date}"
    params = {"adjusted": "false", "sort": "asc", "limit": 50000, "apiKey": POLYGON_API_KEY}

    os.makedirs(CACHE_DIR, exist_ok=True)
    try:
        sd = datetime.strptime(start_date, "%Y-%m-%d").date()
        ed = datetime.strptime(end_date, "%Y-%m-%d").date()
    except Exception:
        sd = None; ed = None
    is_today = (sd == _today_et()) or (ed == _today_et()) if (sd and ed) else False
    key = f"{ticker}_{int(multiplier)}{timespan}_{start_date}_{end_date}.json"
    cache_path = os.path.join(CACHE_DIR, key)
    if (not is_today) and os.path.exists(cache_path):
        try:
            with open(cache_path, 'r') as f:
                data_cached = json.load(f)
            return pd.DataFrame(data_cached)
        except Exception:
            try:
                os.remove(cache_path)
            except Exception:
                pass

    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json() or {}
    results = data.get('results') or []
    if not results:
        return pd.DataFrame()
    rows = []
    for res in results:
        ts = datetime.fromtimestamp(res['t']/1000.0, tz=pytz.utc)
        rows.append({
            'date': ts,
            'open': res.get('o',0),
            'high': res.get('h',0),
            'low': res.get('l',0),
            'close': res.get('c',0),
            'volume': res.get('v',0),
            'vwap': res.get('vw', None),
        })
    df = pd.DataFrame(rows)
    if (not is_today) and not df.empty:
        try:
            with open(cache_path, 'w') as f:
                json.dump(df.to_dict(orient='records'), f, default=str)
        except Exception:
            pass
    return df

def get_polygon_oi_snapshot_today(underlying_ticker: str, expiration_date: date, strikes: list[float]) -> pd.DataFrame:
    """
    Placeholder OI loader for options expiring today. Returns a DataFrame with columns:
    strike, oi_calls, oi_puts, oi_total.
    If a provider endpoint is unavailable, returns an empty DataFrame; callers should handle gracefully.
    """
    try:
        # First prefer cache if available
        cache_dir = os.path.join(CACHE_DIR, "oi")
        os.makedirs(cache_dir, exist_ok=True)
        key = f"{underlying_ticker}_{expiration_date.isoformat()}"
        fp = os.path.join(cache_dir, key + ".csv")
        if (expiration_date != _today_et()) and os.path.exists(fp):
            try:
                return pd.read_csv(fp)
            except Exception:
                pass
        # Fetch from Polygon Options Snapshot: Option Chain Snapshot (recommended for OI)
        POLYGON_API_KEY = os.getenv("POLYGON_API_KEY") or os.getenv("ZE_POLYGON_API_KEY")
        if not POLYGON_API_KEY:
            return pd.DataFrame(columns=["strike", "oi_calls", "oi_puts", "oi_total"])

        base = f"https://api.polygon.io/v3/snapshot/options/{underlying_ticker}"
        params = {
            "expiration_date": expiration_date.strftime("%Y-%m-%d"),
            "limit": 1000,
            "apiKey": POLYGON_API_KEY,
        }
        results = []
        page_guard = 0
        cursor = None
        while True:
            q = params.copy()
            if cursor:
                q["cursor"] = cursor
            r = requests.get(base, params=q, timeout=20)
            r.raise_for_status()
            data = r.json() or {}
            # payload shape can be: { results: [ { strike_price, details: { open_interest }, contract_type, ... }, ...], next_page_token }
            res = data.get("results") or []
            results.extend(res)
            cursor = data.get("next_page_token")
            page_guard += 1
            if not cursor or page_guard > 20:
                break

        if not results:
            return pd.DataFrame(columns=["strike", "oi_calls", "oi_puts", "oi_total"])

        rows = []
        for c in results:
            try:
                strike = float(c.get("strike_price") or c.get("strike", 0))
                # OI field can appear either top-level or nested under details
                details = c.get("details", {}) if isinstance(c.get("details", {}), dict) else {}
                oi_val = c.get("open_interest", None)
                if oi_val is None:
                    oi_val = details.get("open_interest", 0.0)
                side = str(c.get("contract_type", "call")).lower()
                rows.append({"strike": strike, "side": side, "open_interest": float(oi_val or 0.0)})
            except Exception:
                continue
        df = pd.DataFrame(rows)
        if df.empty:
            return pd.DataFrame(columns=["strike", "oi_calls", "oi_puts", "oi_total"])
        piv = df.pivot_table(index="strike", columns="side", values="open_interest", aggfunc="sum", fill_value=0.0)
        piv = piv.rename(columns={"call": "oi_calls", "put": "oi_puts"})
        piv["oi_total"] = piv.get("oi_calls", 0.0) + piv.get("oi_puts", 0.0)
        piv = piv.reset_index()
        # Optional: filter to strikes near the provided list (if any)
        if strikes:
            lo, hi = min(strikes), max(strikes)
            piv = piv[(piv["strike"] >= lo - 5) & (piv["strike"] <= hi + 5)].copy()
        # Save to cache
        if expiration_date != _today_et():
            try:
                piv.to_csv(fp, index=False)
            except Exception:
                pass
        return piv
    except Exception:
        return pd.DataFrame(columns=["strike", "oi_calls", "oi_puts", "oi_total"])
