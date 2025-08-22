# Sigma Core

This document provides a detailed description of the core logic of the Sigma platform.

## Data Module

The Data module contains the core logic for fetching and processing data.

```python
import pandas as pd
from datetime import date

def fetch_0dte_flow(start_date: date, end_date: date, *, ticker: str = "SPY", distance_max: int = 7, workers: int = 8, retries: int = 3, backoff: float = 0.5) -> pd.DataFrame:
    # ...
```

### build_stock_matrix

*   **Function**: `build_stock_matrix(start_date: str, end_date: str, out_csv: str, *, ticker: str = "AAPL", indicator_set_path: str | None = None, label_kind: str | None = None) -> str`
*   **Description**: This function builds a training matrix for a stock. It fetches the hourly data, adds the indicator features, and saves the matrix to a CSV file.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `start_date` | `str` | The start date for the matrix in `YYYY-MM-DD` format. |
| `end_date` | `str` | The end date for the matrix in `YYYY-MM-DD` format. |
| `out_csv` | `str` | The path to the output CSV file. |
| `ticker` | `str` | The ticker symbol of the asset. Defaults to `AAPL`. |
| `indicator_set_path` | `str` \| `None` | The path to the indicator set file. |
| `label_kind` | `str` \| `None` | The kind of label to use for the matrix. |

## Indicators Module

The Indicators module contains the core logic for working with technical indicators.

### IndicatorRegistry

*   **Class**: `IndicatorRegistry`
*   **Description**: This class is a registry for all the technical indicators available in the platform. It automatically discovers and registers all the indicator classes in the `builtins` directory.
*   **Methods**:

| Name | Description |
| --- | --- |
| `register(name: str, indicator_class: Type[Indicator])` | Registers a new indicator. |
| `get(name: str) -> Type[Indicator]` | Returns the indicator class for a given name. |
| `register_builtins()` | Registers all the built-in indicators. |

### get_indicator

*   **Function**: `get_indicator(name: str) -> Type[Indicator]`
*   **Description**: This function returns the indicator class for a given name.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `name` | `str` | The name of the indicator. |

### Indicator

*   **Class**: `Indicator(ABC)`
*   **Description**: This is the base class for all technical indicators. All indicators must inherit from this class and implement the `calculate` method.
*   **Abstract Methods**:

| Name | Description |
| --- | --- |
| `calculate(self, df: pd.DataFrame) -> pd.DataFrame` | Calculates the indicator and returns a DataFrame with the results. |

### Built-in Indicators

This section describes the built-in technical indicators available in the platform.

#### Williams %R

*   **Class**: `WilliamsR(Indicator)`
*   **Description**: This indicator calculates the Williams %R.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `period` | `int` | The window size to use for the Williams %R calculation. Defaults to `14`. |

*   **Output Columns**:

| Name | Type | Description |
| --- | --- | --- |
| `williams_r_{period}` | `float` | The Williams %R value. |

## Features Module

The Features module contains the core logic for building features from raw data.

### IndicatorSpec

*   **Class**: `IndicatorSpec(BaseModel)`
*   **Description**: This class represents the specification of a single indicator within an indicator set.
*   **Attributes**:

| Name | Type | Description |
| --- | --- | --- |
| `name` | `str` | The name of the indicator. |
| `version` | `int` | The version of the indicator. |
| `params` | `Dict[str, Any]` | A dictionary of parameters for the indicator. |

### IndicatorSet

*   **Class**: `IndicatorSet(BaseModel)`
*   **Description**: This class represents a collection of indicator specifications.
*   **Attributes**:

| Name | Type | Description |
| --- | --- | --- |
| `name` | `str` | The name of the indicator set. |
| `version` | `int` | The version of the indicator set. |
| `description` | `str` | A description of the indicator set. |
| `indicators` | `List[IndicatorSpec]` | A list of indicator specifications included in the set. |

### Backtest Registry

#### create_backtest_run

*   **Function**: `create_backtest_run(*, pack_id: str, model_id: str, started_at: Optional[datetime], finished_at: Optional[datetime], params: Dict[str, Any], metrics: Dict[str, Any], plots_uri: Optional[str], data_csv_uri: Optional[str], git_sha: Optional[str] = None, best_sharpe_hourly: Optional[float] = None, best_cum_ret: Optional[float] = None, trades_total: Optional[int] = None, tag: Optional[str] = None) -> Dict[str, Any]`
*   **Description**: This function creates a new backtest run record in the database.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | `str` | The ID of the pack. |
| `model_id` | `str` | The ID of the model. |
| `started_at` | `Optional[datetime]` | The start time of the backtest run. |
| `finished_at` | `Optional[datetime]` | The end time of the backtest run. |
| `params` | `Dict[str, Any]` | A dictionary of parameters used for the backtest. |
| `metrics` | `Dict[str, Any]` | A dictionary of metrics from the backtest. |
| `plots_uri` | `Optional[str]` | The URI to the plots generated by the backtest. |
| `data_csv_uri` | `Optional[str]` | The URI to the data CSV used for the backtest. |
| `git_sha` | `Optional[str]` | The Git SHA of the codebase. |
| `best_sharpe_hourly` | `Optional[float]` | The best hourly Sharpe ratio from the backtest. |
| `best_cum_ret` | `Optional[float]` | The best cumulative return from the backtest. |
| `trades_total` | `Optional[int]` | The total number of trades. |
| `tag` | `Optional[str]` | An optional tag for the backtest run. |

#### leaderboard

*   **Function**: `leaderboard(*, pack_id: Optional[str] = None, model_id: Optional[str] = None, limit: int = 20, order_by: str = "sharpe_hourly", offset: int = 0) -> List[Dict[str, Any]]`
*   **Description**: This function retrieves backtest run records from the database, ordered by a specified metric.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | `Optional[str]` | The ID of the pack to filter by. |
| `model_id` | `Optional[str]` | The ID of the model to filter by. |
| `limit` | `int` | The maximum number of records to return. Defaults to `20`. |
| `order_by` | `str` | The metric to order the results by. Can be `sharpe_hourly` or `cum_ret`. Defaults to `sharpe_hourly`. |
| `offset` | `int` | The number of records to skip. Defaults to `0`. |

#### create_backtest_folds

*   **Function**: `create_backtest_folds(run_id: int, folds: List[Dict[str, Any]]) -> None`
*   **Description**: This function creates new backtest fold records in the database for a given backtest run.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `run_id` | `int` | The ID of the backtest run. |
| `folds` | `List[Dict[str, Any]]` | A list of fold data, where each item is a dictionary containing `fold`, `thr_used`, `cum_ret`, `sharpe_hourly`, and `trades`. |

### Signals Registry

#### upsert_signals

*   **Function**: `upsert_signals(rows: Iterable[Dict[str, Any]]) -> int`
*   **Description**: This function inserts or updates stock signals into the `signals` table. Each row should include at minimum: `date`, `model_id`, `ticker`. Optional fields are persisted when present. On conflict (`date`, `model_id`, `ticker`), it updates core/scoring/exec fields.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `rows` | `Iterable[Dict[str, Any]]` | An iterable of dictionaries, where each dictionary represents a signal. |

#### fetch_signals

*   **Function**: `fetch_signals(*, model_id: Optional[str] = None, pack_id: Optional[str] = None, date_eq: Optional[str] = None, start: Optional[str] = None, end: Optional[str] = None, tickers: Optional[List[str]] = None, limit: int = 200, offset: int = 0) -> List[Dict[str, Any]]`
*   **Description**: This function fetches signals with simple filters. It returns a list of dictionary rows ordered by date descending, rank ascending when present.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | `Optional[str]` | The ID of the model to filter by. |
| `pack_id` | `Optional[str]` | The ID of the pack to filter by. |
| `date_eq` | `Optional[str]` | An exact date to filter by in `YYYY-MM-DD` format. |
| `start` | `Optional[str]` | The start date to filter by in `YYYY-MM-DD` format. |
| `end` | `Optional[str]` | The end date to filter by in `YYYY-MM-DD` format. |
| `tickers` | `Optional[List[str]]` | A list of tickers to include. |
| `limit` | `int` | The maximum number of records to return. Defaults to `200`. |
| `offset` | `int` | The number of records to skip. Defaults to `0`. |

#### upsert_option_signals

*   **Function**: `upsert_option_signals(rows: List[Dict[str, Any]]) -> int`
*   **Description**: This function inserts option overlay rows for signals. It does not update existing records; callers should handle deletion/replacement as needed.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `rows` | `List[Dict[str, Any]]` | A list of dictionaries, where each dictionary represents an option signal. |

#### fetch_option_signals

*   **Function**: `fetch_option_signals(*, model_id: Optional[str] = None, pack_id: Optional[str] = None, date_eq: Optional[str] = None, start: Optional[str] = None, end: Optional[str] = None, tickers: Optional[List[str]] = None, expiry: Optional[str] = None, occ_symbol: Optional[str] = None, limit: int = 200, offset: int = 0) -> List[Dict[str, Any]]`
*   **Description**: This function fetches option overlay rows, optionally filtered by linked signal fields. It joins `option_signals` with `signals` to support various filters and returns a list of dictionary rows ordered by expiry descending, signal_id descending.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | `Optional[str]` | The ID of the model to filter by. |
| `pack_id` | `Optional[str]` | The ID of the pack to filter by. |
| `date_eq` | `Optional[str]` | An exact date to filter by in `YYYY-MM-DD` format. |
| `start` | `Optional[str]` | The start date to filter by in `YYYY-MM-DD` format. |
| `end` | `Optional[str]` | The end date to filter by in `YYYY-MM-DD` format. |
| `tickers` | `Optional[List[str]]` | A list of tickers to include. |
| `expiry` | `Optional[str]` | The expiration date to filter by in `YYYY-MM-DD` format. |
| `occ_symbol` | `Optional[str]` | The OCC symbol to filter by. |
| `limit` | `int` | The maximum number of records to return. Defaults to `200`. |
| `offset` | `int` | The number of records to skip. Defaults to `0`. |

#### replace_option_signals

*   **Function**: `replace_option_signals(rows: List[Dict[str, Any]]) -> int`
*   **Description**: This function replaces option overlay rows for their signal IDs. It deletes existing rows for all signal IDs present in `rows`, then inserts the provided rows.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `rows` | `List[Dict[str, Any]]` | A list of dictionaries, where each dictionary represents an option signal. |



## CV Module

The CV module contains functions for cross-validation.

### Splits

#### PurgedEmbargoedWalkForwardSplit

*   **Class**: `PurgedEmbargoedWalkForwardSplit`
*   **Description**: This class implements a purged and embargoed walk-forward cross-validation split. This splitting method is commonly used in financial time series to prevent look-ahead bias and ensure that the training and testing sets are independent.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `n_splits` | `int` | The number of splits to generate. Defaults to `5`. |
| `embargo` | `float` | The embargo period as a fraction of the test set size. Defaults to `0.0`. |

*   **Methods**:

| Name | Description |
| --- | --- |
| `split(self, X) -> Iterator[Tuple[np.ndarray, np.ndarray]]` | Generates train/test indices for each split. |

## Evaluation Module

The Evaluation module contains functions for evaluating model performance.

### Metrics

#### sharpe_ratio

*   **Function**: `sharpe_ratio(returns, eps: float = 1e-9)`
*   **Description**: This function calculates the Sharpe ratio for a given set of returns.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `returns` | `array` | An array of returns. |
| `eps` | `float` | A small epsilon value to prevent division by zero. Defaults to `1e-9`. |

### Reports

#### to_dict

*   **Function**: `to_dict(obj)`
*   **Description**: This is a skeleton stub function that converts an object to a dictionary. (Note: This is a placeholder and may not reflect full functionality.)
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `obj` | `Any` | The object to convert. |

## Labels Module

The Labels module contains functions for generating labels for training data.

### Hourly Direction

#### label_next_hour_direction

*   **Function**: `label_next_hour_direction(df_hourly: pd.DataFrame, *, k_sigma: float = 0.3, fixed_bp: float | None = None) -> pd.DataFrame`
*   **Description**: This function labels the next-hour direction with an optional flat band determined by `k_sigma * std`. It produces columns `y` (UP/DOWN/FLAT) and `y_syn` (synthetic fallback if `y` missing).
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `df_hourly` | `pd.DataFrame` | The input DataFrame containing hourly data. |
| `k_sigma` | `float` | The sigma value to use for the flat band. Defaults to `0.3`. |
| `fixed_bp` | `float` \| `None` | A fixed basis point value to use for the flat band. |

### Overnight

#### label_close_to_open_direction

*   **Function**: `label_close_to_open_direction(df: pd.DataFrame, *, tz: str = 'US/Eastern') -> pd.DataFrame`
*   **Description**: This function labels each session by the direction from today's close to next day's first bar (approximate open). It produces numeric return `ret_close_to_open` and categorical `y` (UP/DOWN/FLAT) via a small band.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `df` | `pd.DataFrame` | The input DataFrame containing `date` and `close` columns. |
| `tz` | `str` | The timezone to use. Defaults to `US/Eastern`. |

### Forward Returns

#### label_forward_return_days

*   **Function**: `label_forward_return_days(df: pd.DataFrame, *, days: int = 5, classify: bool = True, band: float = 0.001, tz: str = 'US/Eastern') -> pd.DataFrame`
*   **Description**: This function computes forward N-day return labels on an intraday timeline. If `classify` is `True`, it produces categorical `y` (UP/DOWN/FLAT by band) and stores numeric return in `ret_fwd_{days}d`. If `classify` is `False`, it sets `y` to the numeric forward return.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `df` | `pd.DataFrame` | The input DataFrame containing `date` and `close` columns. |
| `days` | `int` | The number of days for the forward return. Defaults to `5`. |
| `classify` | `bool` | Whether to classify the returns into UP/DOWN/FLAT. Defaults to `True`. |
| `band` | `float` | The band to use for classification. Defaults to `0.001`. |
| `tz` | `str` | The timezone to use. Defaults to `US/Eastern`. |

### Zero Sigma Labels

#### label_headfake_reversal

*   **Function**: `label_headfake_reversal(df: pd.DataFrame, *, open_time: str = '09:30', window_end: str = '10:30', min_open_move_atr: float = 0.5, min_reversal_move_atr: float = 0.5, tz: str = 'US/Eastern') -> pd.DataFrame`
*   **Description**: Labels 1 at `window_end` if the open-to-window_end move reverses into the close by at least `min_reversal_move_atr` times the ATR. Emits `y` as 0/1 across all rows of that day, and `y_syn` for compatibility. Requires columns: `date`, `close`; optional `atr_14` or `rolling_std_20` as ATR proxy.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `df` | `pd.DataFrame` | The input DataFrame. |
| `open_time` | `str` | The opening time of the trading session. Defaults to `09:30`. |
| `window_end` | `str` | The end time of the window. Defaults to `10:30`. |
| `min_open_move_atr` | `float` | The minimum open move in ATR units. Defaults to `0.5`. |
| `min_reversal_move_atr` | `float` | The minimum reversal move in ATR units. Defaults to `0.5`. |
| `tz` | `str` | The timezone to use. Defaults to `US/Eastern`. |

#### label_pin_drift

*   **Function**: `label_pin_drift(df: pd.DataFrame, *, drift_start_time: str = '15:00', min_pull_atr: float = 0.2, tz: str = 'US/Eastern') -> pd.DataFrame`
*   **Description**: Labels 1 if price drifts toward the nearest OI/gamma peak from `drift_start_time` to close by at least `min_pull_atr` times the ATR. Requires `close`, `date`; optional `oi_peak_strike` or `gamma_peak_strike` and `atr_14` or `rolling_std_20`.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `df` | `pd.DataFrame` | The input DataFrame. |
| `drift_start_time` | `str` | The start time of the drift. Defaults to `15:00`. |
| `min_pull_atr` | `float` | The minimum pull in ATR units. Defaults to `0.2`. |
| `tz` | `str` | The timezone to use. Defaults to `US/Eastern`. |

## Live Module

The Live module contains components for live trading and event handling.

### Events

#### SignalEvent

*   **Class**: `SignalEvent`
*   **Description**: This is a skeleton class representing a signal event. (Note: This is a placeholder and may not reflect full functionality.)

### Execution

#### submit_order

*   **Function**: `submit_order(symbol: str, side: str, qty: float)`
*   **Description**: This is a skeleton stub function for submitting an order. (Note: This is a placeholder and may not reflect full functionality.)
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `symbol` | `str` | The symbol of the asset to trade. |
| `side` | `str` | The side of the trade (e.g., `buy`, `sell`). |
| `qty` | `float` | The quantity to trade. |

### Runtime

#### run_once

*   **Function**: `run_once()`
*   **Description**: This is a skeleton stub function for running a single iteration of the live trading system. (Note: This is a placeholder and may not reflect full functionality.)

## Models Module

The Models module contains components for working with machine learning models.

### Interfaces

#### PredictProba

*   **Protocol**: `PredictProba(Protocol)`
*   **Description**: This is a skeleton protocol for models that implement a `predict_proba` method. (Note: This is a placeholder and may not reflect full functionality.)

### GBM

#### main

*   **Function**: `main()`
*   **Description**: This function trains an XGBoost model for 0DTE hourly direction. It reads a training CSV, filters by allowed hours, trains the model, and saves it to a file.
*   **Command Line Arguments**:

| Name | Type | Description |
| --- | --- | --- |
| `--csv` | `str` | Path to training CSV (matrix). Defaults to `train_sample.csv`. |
| `--target` | `str` | Target column: `y` or `y_syn` (auto if not provided). |
| `--model_out` | `str` | Output path for model. Defaults to `models/gbm_0dte.pkl`. |
| `--splits` | `int` | Number of walk-forward splits. Defaults to `3`. |
| `--allowed_hours` | `str` | Comma-separated ET hours to include (e.g., `13,14,15`). |

### Model Registry

#### ModelRegistry

*   **Class**: `ModelRegistry`
*   **Description**: This class provides methods for interacting with the `model_versions` table in the database, allowing you to create, retrieve, and list model versions.
*   **Methods**:

| Name | Description |
| --- | --- |
| `create_model_version(self, name: str, version: str, description: str, artifact_uri: str, data_hash: str, git_sha: str, metrics: dict) -> ModelVersion` | Creates a new model version record in the database. |
| `get_model_version(self, name: str, version: str) -> Optional[ModelVersion]` | Retrieves a specific model version from the database. |
| `list_model_versions(self) -> List[ModelVersion]` | Lists all model versions in the database. |

## Orchestration Module

The Orchestration module contains functions for defining and managing orchestration jobs.

### Jobs

#### backtest_job

*   **Function**: `backtest_job()`
*   **Description**: This is a skeleton stub function representing a backtest job. (Note: This is a placeholder and may not reflect full functionality.)

### Temporal/Dagster Integration

*   **File**: `products/sigma-core/sigma_core/orchestration/temporal_dagster.py`
*   **Description**: This file is a skeleton for binding the orchestration jobs to Temporal/Dagster. (Note: This is a placeholder and may not reflect full functionality.)

## Services Module

The Services module contains various helper functions and utilities.

### IO

#### workspace_paths

*   **Function**: `workspace_paths(model_id: str, pack_id: str = "zerosigma") -> Dict[str, Path]`
*   **Description**: This function returns a dictionary of file paths for a given model and pack. These paths include locations for matrices, live data, artifacts, reports, plots, policies, and configurations.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | `str` | The ID of the model. |
| `pack_id` | `str` | The ID of the pack. Defaults to `zerosigma`. |

#### load_config

*   **Function**: `load_config(model_id: str, pack_id: str = "zerosigma") -> Dict[str, Any]`
*   **Description**: This function loads the configuration for a given model and pack from a YAML file.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | `str` | The ID of the model. |
| `pack_id` | `str` | The ID of the pack. Defaults to `zerosigma`. |

#### resolve_indicator_set_path

*   **Function**: `resolve_indicator_set_path(pack_id: str, model_id: str, indicator_set_name: Optional[str] = None) -> Path`
*   **Description**: This function resolves the path to an indicator set file for a given pack and model. It checks for a model-specific indicator set, then a named indicator set, and finally a legacy indicator set.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | `str` | The ID of the pack. |
| `model_id` | `str` | The ID of the model. |
| `indicator_set_name` | `Optional[str]` | The name of the indicator set. |

#### sanitize_out_path

*   **Function**: `sanitize_out_path(candidate: Optional[str], default_path: Path) -> Path`
*   **Description**: This function sanitizes an output path to ensure it is within the allowed product workspace. It also creates the parent directory if it does not exist.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `candidate` | `Optional[str]` | The candidate output path. |
| `default_path` | `Path` | The default path to use if the candidate is not provided. |

### Lineage

#### compute_lineage

*   **Function**: `compute_lineage(*, pack_dir: Path, model_id: str, indicator_set_path: Optional[Path] = None) -> Dict[str, Optional[str]]`
*   **Description**: This function computes the lineage (SHA hashes) of various files related to a model, including the pack, indicator set, model configuration, and policy.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_dir` | `Path` | The path to the pack directory. |
| `model_id` | `str` | The ID of the model. |
| `indicator_set_path` | `Optional[Path]` | The path to the indicator set file. |

### Model Cards

#### write_model_card

*   **Function**: `write_model_card(*, pack_id: str, model_id: str, event: str, params: Optional[Dict[str, Any]] = None, metrics: Optional[Dict[str, Any]] = None, features: Optional[List[str]] = None, lineage: Optional[Dict[str, Optional[str]]] = None, notes: Optional[str] = None) -> Dict[str, str]`
*   **Description**: This function writes a model card (both JSON and Markdown) for a given model and event. A model card contains information about the model's configuration, parameters, metrics, features, and lineage.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | `str` | The ID of the pack. |
| `model_id` | `str` | The ID of the model. |
| `event` | `str` | The event that triggered the model card creation (e.g., `train`, `backtest`). |
| `params` | `Optional[Dict[str, Any]]` | A dictionary of parameters used for the event. |
| `metrics` | `Optional[Dict[str, Any]]` | A dictionary of metrics from the event. |
| `features` | `Optional[List[str]]` | A list of features used by the model. |
| `lineage` | `Optional[Dict[str, Optional[str]]]` | A dictionary of lineage information. |
| `notes` | `Optional[str]` | Additional notes for the model card. |

#### list_model_cards

*   **Function**: `list_model_cards(*, pack_id: str, model_id: str) -> List[Dict[str, Any]]`
*   **Description**: This function lists all model cards for a given model.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | `str` | The ID of the pack. |
| `model_id` | `str` | The ID of the model. |

#### load_model_card

*   **Function**: `load_model_card(*, pack_id: str, model_id: str, file: Optional[str] = None) -> Dict[str, Any]`
*   **Description**: This function loads a model card (both JSON and Markdown) for a given model. If no file is specified, it loads the latest model card.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | `str` | The ID of the pack. |
| `model_id` | `str` | The ID of the model. |
| `file` | `Optional[str]` | The name of the model card file to load. |

### Policy

#### load_policy

*   **Function**: `load_policy(model_id: str, pack_id: str) -> Dict[str, Any]`
*   **Description**: This function loads the policy for a given model and pack from a YAML file.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | `str` | The ID of the model. |
| `pack_id` | `str` | The ID of the pack. |

#### validate_policy_file

*   **Function**: `validate_policy_file(path: _Path) -> (bool, List[str])`
*   **Description**: This function validates the schema of a policy file. It returns a boolean indicating whether the policy is valid and a list of any errors.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `path` | `_Path` | The path to the policy file. |

#### ensure_policy_exists

*   **Function**: `ensure_policy_exists(model_id: str, pack_id: str) -> Optional[str]`
*   **Description**: This function ensures that a policy file exists for a given model and pack, and that it is valid. If the policy file is missing or invalid, it returns an error message.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | `str` | The ID of the model. |
| `pack_id` | `str` | The ID of the pack. |

### Signals Live



## Storage Module

The Storage module contains functions for interacting with the database.

### Relational

#### Database

*   **Class**: `Database`
*   **Description**: This class manages the database connection pool. It ensures that `psycopg2` is installed and that the necessary environment variables for database connection are set.
*   **Methods**:

| Name | Description |
| --- | --- |
| `_ensure_pool(self)` | Ensures that the connection pool is initialized. |
| `get_connection(self)` | A context manager that provides a database connection from the pool. |

#### get_db

*   **Function**: `get_db()`
*   **Description**: This is a context manager that provides a database connection. It ensures that `psycopg2` is installed and that the necessary environment variables for database connection are set.


## Registry Module

The Registry module contains functions for interacting with the database registries.

### Backtest Registry

#### create_backtest_run

*   **Function**: `create_backtest_run(*, pack_id: str, model_id: str, started_at: Optional[datetime], finished_at: Optional[datetime], params: Dict[str, Any], metrics: Dict[str, Any], plots_uri: Optional[str], data_csv_uri: Optional[str], git_sha: Optional[str] = None, best_sharpe_hourly: Optional[float] = None, best_cum_ret: Optional[float] = None, trades_total: Optional[int] = None, tag: Optional[str] = None) -> Dict[str, Any]`
*   **Description**: This function creates a new backtest run record in the database.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | `str` | The ID of the pack. |
| `model_id` | `str` | The ID of the model. |
| `started_at` | `Optional[datetime]` | The start time of the backtest run. |
| `finished_at` | `Optional[datetime]` | The end time of the backtest run. |
| `params` | `Dict[str, Any]` | A dictionary of parameters used for the backtest. |
| `metrics` | `Dict[str, Any]` | A dictionary of metrics from the backtest. |
| `plots_uri` | `Optional[str]` | The URI to the plots generated by the backtest. |
| `data_csv_uri` | `Optional[str]` | The URI to the data CSV used for the backtest. |
| `git_sha` | `Optional[str]` | The Git SHA of the codebase. |
| `best_sharpe_hourly` | `Optional[float]` | The best hourly Sharpe ratio from the backtest. |
| `best_cum_ret` | `Optional[float]` | The best cumulative return from the backtest. |
| `trades_total` | `Optional[int]` | The total number of trades. |
| `tag` | `Optional[str]` | An optional tag for the backtest run. |

#### leaderboard

*   **Function**: `leaderboard(*, pack_id: Optional[str] = None, model_id: Optional[str] = None, limit: int = 20, order_by: str = "sharpe_hourly", offset: int = 0) -> List[Dict[str, Any]]`
*   **Description**: This function retrieves backtest run records from the database, ordered by a specified metric.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | `Optional[str]` | The ID of the pack to filter by. |
| `model_id` | `Optional[str]` | The ID of the model to filter by. |
| `limit` | `int` | The maximum number of records to return. Defaults to `20`. |
| `order_by` | `str` | The metric to order the results by. Can be `sharpe_hourly` or `cum_ret`. Defaults to `sharpe_hourly`. |
| `offset` | `int` | The number of records to skip. Defaults to `0`. |

#### create_backtest_folds

*   **Function**: `create_backtest_folds(run_id: int, folds: List[Dict[str, Any]]) -> None`
*   **Description**: This function creates new backtest fold records in the database for a given backtest run.
*   **Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `run_id` | `int` | The ID of the backtest run. |
| `folds` | `List[Dict[str, Any]]` | A list of fold data, where each item is a dictionary containing `fold`, `thr_used`, `cum_ret`, `sharpe_hourly`, and `trades`. |
