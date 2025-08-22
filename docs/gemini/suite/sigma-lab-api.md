# Sigma Lab API

This document provides a detailed description of the Sigma Lab API. The API is organized around a set of RESTful endpoints that allow you to interact with the different components of the Sigma Lab platform.

## Models Router

The Models router provides endpoints for creating, managing, and backtesting trading models.

### Create a new model

*   **Endpoint**: `POST /models`
*   **Description**: This endpoint allows you to create a new trading model. You can specify the ticker, asset type, horizon, cadence, and other parameters for the model. The endpoint will create a new directory for the model and a default configuration file.
*   **Request Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ticker` | string | The ticker symbol of the asset to trade. |
| `asset_type` | string | The type of asset to trade. Can be `opt` for options or `eq` for equities. Defaults to `opt`. |
| `horizon` | string | The trading horizon. Can be `0dte`, `intraday`, `swing`, or `long`. Defaults to `0dte`. |
| `cadence` | string | The trading cadence. Can be `5m`, `15m`, `hourly`, or `daily`. Defaults to `hourly`. |
| `algo` | string | The algorithm to use for the model. Defaults to `gbm`. |
| `variant` | string | An optional variant name to append to the model ID. |
| `pack_id` | string | The ID of the pack to associate the model with. Defaults to `zerosigma`. |
| `indicator_set_name` | string | The name of the indicator set to use for the model. |

*   **Example Request**:

```json
{
  "ticker": "SPY",
  "asset_type": "opt",
  "horizon": "0dte",
  "cadence": "hourly",
  "pack_id": "zerosigma"
}
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `model_id` | string | The ID of the newly created model. |
| `paths` | object | An object containing the paths to the model's configuration and policy files. |
| `message` | string | A message indicating that the model was created successfully. |

*   **Example Response**:

```json
{
  "ok": true,
  "model_id": "spy_opt_0dte_hourly",
  "paths": {
    "config": "packs/zerosigma/model_configs/spy_opt_0dte_hourly.yaml",
    "policy": "packs/zerosigma/policies/spy_opt_0dte_hourly.yaml"
  },
  "message": "created"
}
```

### Upsert an indicator set

*   **Endpoint**: `POST /indicator_sets`
*   **Description**: This endpoint allows you to create or update an indicator set. An indicator set is a collection of indicators that can be used in a trading model.
*   **Request Body**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack to associate the indicator set with. |
| `scope` | string | The scope of the indicator set. Can be `pack` or `model`. Defaults to `pack`. |
| `model_id` | string | The ID of the model to associate the indicator set with. Required if `scope` is `model`. |
| `name` | string | The name of the indicator set. |
| `indicators` | array | An array of indicators to include in the set. Each indicator can be a string or an object with a `name` and `params`. |

*   **Example Request**:

```json
{
  "pack_id": "zerosigma",
  "scope": "pack",
  "name": "my_indicator_set",
  "indicators": [
    "rsi__period=14",
    {
      "name": "macd",
      "fast_period": 12,
      "slow_period": 26,
      "signal_period": 9
    }
  ]
}
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `path` | string | The path to the indicator set file. |
| `count` | integer | The number of indicators in the set. |
| `message` | string | A message indicating that the indicator set was written successfully. |

*   **Example Response**:

```json
{
  "ok": true,
  "path": "packs/zerosigma/indicator_sets/my_indicator_set.yaml",
  "count": 2,
  "message": "written"
}
```

### List all models

*   **Endpoint**: `GET /models`
*   **Description**: This endpoint returns a list of all available trading models. You can optionally filter the list by pack ID.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack to filter by. If not provided, all models will be returned. |

*   **Example Request**:

```
GET /models?pack_id=zerosigma
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `models` | array | An array of model objects. |
| `count` | integer | The number of models returned. |

*   **Example Response**:

```json
{
  "ok": true,
  "models": [
    {
      "id": "spy_opt_0dte_hourly",
      "pack_id": "zerosigma",
      "path": "packs/zerosigma/model_configs/spy_opt_0dte_hourly.yaml"
    }
  ],
  "count": 1
}
```

### Preview a training matrix

*   **Endpoint**: `POST /preview_matrix`
*   **Description**: This endpoint allows you to preview a training matrix for a given model and date range. The training matrix is a table of data that is used to train a trading model.
*   **Request Body**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to preview the matrix for. |
| `start` | string | The start date for the matrix in `YYYY-MM-DD` format. |
| `end` | string | The end date for the matrix in `YYYY-MM-DD` format. |
| `pack_id` | string | The ID of the pack the model belongs to. Defaults to `zerosigma`. |
| `max_rows` | integer | The maximum number of rows to return in the preview. Defaults to `200`. |

*   **Example Request**:

```json
{
  "model_id": "spy_opt_0dte_hourly",
  "start": "2024-01-01",
  "end": "2024-01-31",
  "pack_id": "zerosigma"
}
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `rows` | integer | The number of rows in the matrix. |
| `qa` | object | An object containing the results of a quality assurance check on the matrix. |
| `nan_stats` | array | An array of objects containing statistics about the percentage of `NaN` values in each column. |
| `warn` | array | An array of columns with a high percentage of `NaN` values. |
| `fail` | array | An array of columns with a very high percentage of `NaN` values. |

*   **Example Response**:

```json
{
  "ok": true,
  "rows": 1000,
  "qa": {
    "monotonic_time": {
      "ok": true,
      "violations": 0
    },
    "non_negative_vol": {
      "ok": true,
      "neg_pct": 0,
      "checked": 1000
    },
    "session_alignment": {
      "ok": true,
      "off_pct": 0
    },
    "iv_sanity": {
      "ok": true,
      "out_of_range_pct": 0,
      "checked": 1000
    },
    "nan": {
      "warn": [],
      "fail": []
    }
  },
  "nan_stats": [
    {
      "column": "rsi_14",
      "nan_pct": 0
    }
  ],
  "warn": [],
  "fail": []
}
```

### Update a model config

*   **Endpoint**: `PATCH /models/{model_id}`
*   **Description**: This endpoint allows you to update the configuration of a trading model.
*   **Path Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to update. |

*   **Request Body**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack the model belongs to. Defaults to `zerosigma`. |
| `config` | object | A partial configuration object to merge into the existing configuration. |

*   **Example Request**:

```json
{
  "pack_id": "zerosigma",
  "config": {
    "hyperparams": {
      "max_depth": 8
    }
  }
}
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `path` | string | The path to the model's configuration file. |
| `config` | object | The updated configuration object. |

*   **Example Response**:

```json
{
  "ok": true,
  "path": "packs/zerosigma/model_configs/spy_opt_0dte_hourly.yaml",
  "config": {
    "model_id": "spy_opt_0dte_hourly",
    "ticker": "SPY",
    "model": "gbm",
    "task": "classification",
    "hyperparams": {
      "n_estimators": 300,
      "max_depth": 8,
      "learning_rate": 0.05
    },
    "features": [
      "rsi__period=14",
      "iv_realized_spread__window=20",
      "sold_flow_ratio__window=5"
    ],
    "label": {
      "type": "next_bar_updown",
      "horizon": 1
    },
    "train_window": {
      "start": "2023-01-01",
      "end": "2024-12-31"
    },
    "asset_type": "opt",
    "horizon": "0dte",
    "cadence": "hourly"
  }
}
```

### List all model templates

*   **Endpoint**: `GET /model_templates`
*   **Description**: This endpoint returns a list of all available model templates. You can optionally filter the list by pack ID.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack` | string | The ID of the pack to filter by. If not provided, all templates will be returned. |

*   **Example Request**:

```
GET /model_templates?pack=zerosigma
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `templates` | array | An array of template objects. |

*   **Example Response**:

```json
{
  "ok": true,
  "templates": [
    {
      "pack": "zerosigma",
      "template_id": "0dte_hourly_options",
      "name": "0DTE Hourly Options",
      "horizon": "0dte",
      "cadence": "hourly",
      "template_version": 1
    }
  ]
}
```

## Backtest Router

The Backtest router provides endpoints for running backtests and viewing the results.

### Run a backtest

*   **Endpoint**: `POST /backtest`
*   **Description**: This endpoint allows you to run a backtest for a given model.
*   **Request Body**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to backtest. |
| `csv` | string | The path to the training matrix CSV file. If not provided, the default training matrix for the model will be used. |
| `target` | string | The name of the target column in the training matrix. Defaults to `y` or `y_syn`. |
| `thresholds` | string or array | A comma-separated string or an array of floats representing the prediction thresholds to use for the backtest. |
| `splits` | integer | The number of splits to use for cross-validation. Defaults to `5`. |
| `embargo` | float | The embargo percentage to use for cross-validation. Defaults to `0.0`. |
| `top_pct` | float | The percentage of top predictions to use for the backtest. |
| `allowed_hours` | string or array | A comma-separated string or an array of integers representing the hours of the day to allow trading. |
| `slippage_bps` | float | The slippage in basis points to use for the backtest. Defaults to `1.0`. |
| `size_by_conf` | boolean | Whether to size trades by the confidence of the prediction. Defaults to `false`. |
| `conf_cap` | float | The maximum confidence to use for sizing trades. Defaults to `1.0`. |
| `per_hour_thresholds` | boolean | Whether to use per-hour thresholds for the backtest. Defaults to `false`. |
| `per_hour_select_by` | string | The metric to use for selecting the best per-hour threshold. Can be `sharpe`, `cum_ret`, or `trades`. Defaults to `sharpe`. |
| `calibration` | string | The type of calibration to use for the predictions. Can be `none`, `sigmoid`, or `isotonic`. |
| `pack_id` | string | The ID of the pack the model belongs to. Defaults to `zerosigma`. |
| `momentum_gate` | boolean | Whether to use a momentum gate to filter trades. |
| `momentum_min` | float | The minimum momentum required to enter a trade. |
| `momentum_column` | string | The name of the momentum column in the training matrix. |
| `save` | boolean | Whether to save the backtest results to the database. Defaults to `true`. |
| `tag` | string | An optional tag to associate with the backtest run. |

*   **Example Request**:

```json
{
  "model_id": "spy_opt_0dte_hourly",
  "thresholds": "0.55,0.60,0.65",
  "splits": 5
}
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `result` | object | An object containing the results of the backtest. |
| `best_sharpe_hourly` | float | The best hourly Sharpe ratio achieved in the backtest. |
| `best_cum_ret` | float | The best cumulative return achieved in the backtest. |
| `parity` | object | An object containing the results of a parity backtest for options. |

*   **Example Response**:

```json
{
  "ok": true,
  "result": {
    "threshold_results": [
      {
        "thr": 0.55,
        "cum_ret": 0.12,
        "sharpe_hourly": 1.2,
        "trades": 100
      }
    ]
  },
  "best_sharpe_hourly": 1.2,
  "best_cum_ret": 0.12,
  "parity": null
}
```

### Get the leaderboard

*   **Endpoint**: `GET /leaderboard`
*   **Description**: This endpoint returns a leaderboard of the top-performing backtests.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack to filter by. |
| `model_id` | string | The ID of the model to filter by. |
| `limit` | integer | The maximum number of results to return. Defaults to `20`. |
| `order_by` | string | The metric to order the results by. Defaults to `sharpe_hourly`. |
| `offset` | integer | The number of results to skip. Defaults to `0`. |
| `tag` | string | An optional tag to filter the results by. |

*   **Example Request**:

```
GET /leaderboard?pack_id=zerosigma&limit=10
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `rows` | array | An array of leaderboard objects. |
| `limit` | integer | The maximum number of results returned. |
| `offset` | integer | The number of results skipped. |
| `next_offset` | integer | The offset to use for the next page of results. |
| `tag` | string | The tag that was used to filter the results. |

*   **Example Response**:

```json
{
  "ok": true,
  "rows": [
    {
      "id": 1,
      "pack_id": "zerosigma",
      "model_id": "spy_opt_0dte_hourly",
      "best_sharpe_hourly": 1.2,
      "best_cum_ret": 0.12,
      "tag": "my_backtest"
    }
  ],
  "limit": 10,
  "offset": 0,
  "next_offset": 1,
  "tag": "my_backtest"
}
```

## Admin Router

The Admin router provides endpoints for managing the administrative functions of the platform. **Note:** These endpoints are not yet implemented and will return a `501 Not Implemented` error.

### Get all jobs

*   **Endpoint**: `GET /admin/jobs`
*   **Description**: This endpoint is intended to return a list of all background jobs.
*   **Status**: Not Implemented

### Retry a job

*   **Endpoint**: `POST /admin/jobs/{job_id}/retry`
*   **Description**: This endpoint is intended to retry a failed background job.
*   **Status**: Not Implemented

### Cancel a job

*   **Endpoint**: `POST /admin/jobs/{job_id}/cancel`
*   **Description**: This endpoint is intended to cancel a running background job.
*   **Status**: Not Implemented

### Get all quotas

*   **Endpoint**: `GET /admin/quotas`
*   **Description**: This endpoint is intended to return a list of all user quotas.
*   **Status**: Not Implemented

### Update quotas

*   **Endpoint**: `PATCH /admin/quotas`
*   **Description**: This endpoint is intended to update user quotas.
*   **Status**: Not Implemented

### Get all risk profiles

*   **Endpoint**: `GET /admin/risk-profiles`
*   **Description**: This endpoint is intended to return a list of all risk profiles.
*   **Status**: Not Implemented

### Update risk profiles

*   **Endpoint**: `PATCH /admin/risk-profiles`
*   **Description**: This endpoint is intended to update risk profiles.
*   **Status**: Not Implemented

### Get all packs

*   **Endpoint**: `GET /admin/packs`
*   **Description**: This endpoint is intended to return a list of all packs.
*   **Status**: Not Implemented

### Get all indicator sets

*   **Endpoint**: `GET /admin/indicator_sets`
*   **Description**: This endpoint is intended to return a list of all indicator sets.
*   **Status**: Not Implemented

### Get all templates

*   **Endpoint**: `GET /admin/templates`
*   **Description**: This endpoint is intended to return a list of all model templates.
*   **Status**: Not Implemented

### Create a template

*   **Endpoint**: `POST /admin/templates`
*   **Description**: This endpoint is intended to create a new model template.
*   **Status**: Not Implemented

### Update a template

*   **Endpoint**: `PATCH /admin/templates/{template_id}`
*   **Description**: This endpoint is intended to update a model template.
*   **Status**: Not Implemented

### Publish a template

*   **Endpoint**: `POST /admin/templates/{template_id}/publish`
*   **Description**: This endpoint is intended to publish a model template to the Sigma Market.
*   **Status**: Not Implemented

### Get all feature flags

*   **Endpoint**: `GET /admin/flags`
*   **Description**: This endpoint is intended to return a list of all feature flags.
*   **Status**: Not Implemented

### Update feature flags

*   **Endpoint**: `PATCH /admin/flags`
*   **Description**: This endpoint is intended to update feature flags.
*   **Status**: Not Implemented

### Get system health

*   **Endpoint**: `GET /admin/health`
*   **Description**: This endpoint is intended to return the health status of the system.
*   **Status**: Not Implemented

### Get audit log

*   **Endpoint**: `GET /admin/audit`
*   **Description**: This endpoint is intended to return the audit log.
*   **Status**: Not Implemented

### Get all users

*   **Endpoint**: `GET /admin/users`
*   **Description**: This endpoint is intended to return a list of all users.
*   **Status**: Not Implemented

### Update a user

*   **Endpoint**: `PATCH /admin/users/{user_id}`
*   **Description**: This endpoint is intended to update a user.
*   **Status**: Not Implemented

### Rotate a user token

*   **Endpoint**: `POST /admin/users/{user_id}/rotate_token`
*   **Description**: This endpoint is intended to rotate a user's API token.
*   **Status**: Not Implemented

## Audit Router

The Audit router provides endpoints for viewing the audit log.

### Get the audit log

*   **Endpoint**: `GET /audit`
*   **Description**: This endpoint returns a list of audit log entries. You can filter the list by a variety of parameters.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `path` | string | The path of the request to filter by. |
| `method` | string | The HTTP method of the request to filter by. |
| `status` | integer | The HTTP status code of the response to filter by. |
| `pack_id` | string | The ID of the pack to filter by. |
| `model_id` | string | The ID of the model to filter by. |
| `start` | string | The start date for the audit log in `YYYY-MM-DD` format. |
| `end` | string | The end date for the audit log in `YYYY-MM-DD` format. |
| `limit` | integer | The maximum number of results to return. Defaults to `100`. |
| `offset` | integer | The number of results to skip. Defaults to `0`. |

*   **Example Request**:

```
GET /audit?pack_id=zerosigma&limit=10
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `rows` | array | An array of audit log objects. |
| `count` | integer | The number of audit log entries returned. |
| `limit` | integer | The maximum number of results returned. |
| `offset` | integer | The number of results skipped. |
| `next_offset` | integer | The offset to use for the next page of results. |

*   **Example Response**:

```json
{
  "ok": true,
  "rows": [
    {
      "id": 1,
      "created_at": "2025-08-21T12:00:00Z",
      "path": "/models",
      "method": "POST",
      "status": 200,
      "pack_id": "zerosigma",
      "model_id": "spy_opt_0dte_hourly"
    }
  ],
  "count": 1,
  "limit": 10,
  "offset": 0,
  "next_offset": 1
}
```

## Calibration Router

The Calibration router provides endpoints for calibrating the parameters of a trading model.

### Calibrate thresholds

*   **Endpoint**: `POST /calibrate_thresholds`
*   **Description**: This endpoint helps you to find the optimal prediction threshold for a given model and metric.
*   **Request Body**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to calibrate. |
| `csv` | string | The path to the training matrix CSV file. If not provided, the default training matrix for the model will be used. |
| `pack_id` | string | The ID of the pack the model belongs to. |
| `metric` | string | The metric to optimize for. Defaults to `sharpe`. |
| `column` | string | The name of the prediction score column in the training matrix. Defaults to `score_total`. |
| `grid` | string | A comma-separated string of threshold values to test. |
| `top_n` | integer | The desired number of trades to generate. |

*   **Example Request**:

```json
{
  "model_id": "spy_opt_0dte_hourly",
  "top_n": 50
}
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `model_id` | string | The ID of the model that was calibrated. |
| `source_csv` | string | The path to the CSV file that was used for calibration. |
| `column` | string | The name of the prediction score column that was used. |
| `top_n` | integer | The desired number of trades. |
| `grid` | array | An array of the threshold values that were tested. |
| `counts` | array | An array of objects containing the number of trades generated for each threshold. |
| `recommended_threshold` | float | The recommended threshold value. |
| `expected_count` | integer | The expected number of trades at the recommended threshold. |

*   **Example Response**:

```json
{
  "ok": true,
  "model_id": "spy_opt_0dte_hourly",
  "source_csv": "matrices/spy_opt_0dte_hourly/training_matrix_built.csv",
  "column": "score_total",
  "top_n": 50,
  "grid": [
    0.5,
    0.55,
    0.6,
    0.65,
    0.7
  ],
  "counts": [
    {
      "threshold": 0.5,
      "count": 100
    },
    {
      "threshold": 0.55,
      "count": 75
    },
    {
      "threshold": 0.6,
      "count": 52
    },
    {
      "threshold": 0.65,
      "count": 30
    },
    {
      "threshold": 0.7,
      "count": 15
    }
  ],
  "recommended_threshold": 0.6,
  "expected_count": 52
}
```

### Calibrate brackets

*   **Endpoint**: `POST /calibrate_brackets`
*   **Description**: This endpoint helps you to find the optimal ATR-based bracket parameters for a given model and desired risk:reward ratio.
*   **Request Body**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to calibrate. |
| `pack_id` | string | The ID of the pack the model belongs to. Defaults to `swingsigma`. |
| `desired_rr` | float | The desired risk:reward ratio. Defaults to `2.0`. |
| `k_stop_grid` | string | A comma-separated string of ATR multiplier values for the stop loss to test. |
| `k_target_grid` | string | A comma-separated string of ATR multiplier values for the take profit to test. |
| `time_stop_candidates` | string | A comma-separated string of time stop values in minutes to test. |

*   **Example Request**:

```json
{
  "model_id": "spy_eq_swing_daily",
  "desired_rr": 2.5
}
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `desired_rr` | float | The desired risk:reward ratio. |
| `recommended` | object | An object containing the recommended bracket parameters. |
| `candidates` | array | An array of candidate bracket parameter objects. |
| `note` | string | A note about the calibration process. |

*   **Example Response**:

```json
{
  "ok": true,
  "desired_rr": 2.5,
  "recommended": {
    "atr_mult_stop": 1.2,
    "atr_mult_target": 3,
    "rr_implied": 2.5,
    "time_stop_minutes": 120
  },
  "candidates": [
    {
      "k_stop": 1.2,
      "k_target": 3,
      "rr": 2.5,
      "delta": 0
    }
  ],
  "note": "RR under ATR brackets is k_target/k_stop (constant per-row). Consider regime-aware adjustments later."
}
```

## Datasets Router

The Datasets router provides endpoints for building training matrices.

### Build a training matrix

*   **Endpoint**: `POST /build_matrix`
*   **Description**: This endpoint allows you to build a training matrix for a given model and date range.
*   **Request Body**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to build the matrix for. |
| `start` | string | The start date for the matrix in `YYYY-MM-DD` format. |
| `end` | string | The end date for the matrix in `YYYY-MM-DD` format. |
| `out_csv` | string | The path to the output CSV file. If not provided, a default path will be used. |
| `pack_id` | string | The ID of the pack the model belongs to. Defaults to `zerosigma`. |
| `k_sigma` | float | The sigma value to use for the matrix. Defaults to `0.3`. |
| `fixed_bp` | float | The fixed basis points to use for the matrix. |
| `distance_max` | integer | The maximum distance to use for the matrix. Defaults to `7`. |
| `dump_raw` | boolean | Whether to dump the raw data to a separate CSV file. Defaults to `false`. |
| `raw_out` | string | The path to the output CSV file for the raw data. |
| `ticker` | string | The ticker symbol of the asset to build the matrix for. |

*   **Example Request**:

```json
{
  "model_id": "spy_opt_0dte_hourly",
  "start": "2024-01-01",
  "end": "2024-01-31"
}
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `out_csv` | string | The path to the output CSV file. |

*   **Example Response**:

```json
{
  "ok": true,
  "out_csv": "matrices/spy_opt_0dte_hourly/training_matrix_built.csv"
}
```

### Build a stock training matrix

*   **Endpoint**: `POST /build_stock_matrix`
*   **Description**: This endpoint allows you to build a training matrix for a stock.
*   **Request Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ticker` | string | The ticker symbol of the stock to build the matrix for. |
| `start` | string | The start date for the matrix in `YYYY-MM-DD` format. |
| `end` | string | The end date for the matrix in `YYYY-MM-DD` format. |
| `out_csv` | string | The path to the output CSV file. If not provided, a default path will be used. |
| `pack_id` | string | The ID of the pack to associate the matrix with. |
| `model_id` | string | The ID of the model to associate the matrix with. |
| `label_kind` | string | The kind of label to use for the matrix. |

*   **Example Request**:

```json
{
  "ticker": "AAPL",
  "start": "2024-01-01",
  "end": "2024-01-31"
}
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `out_csv` | string | The path to the output CSV file. |

*   **Example Response**:

```json
{
  "ok": true,
  "out_csv": "matrices/aapl/stock_matrix.csv"
}
```

## Health Router

The Health router provides endpoints for checking the health of the platform.

### Get health status

*   **Endpoint**: `GET /health`
*   **Description**: This endpoint returns a simple health check to confirm that the API is running.
*   **Example Request**:

```
GET /health
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the API is running. |

*   **Example Response**:

```json
{
  "ok": true
}
```

### Get detailed health status

*   **Endpoint**: `GET /healthz`
*   **Description**: This endpoint returns a detailed health check of the platform, including the status of the database, Polygon API, and other dependencies.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `ticker` | string | The ticker symbol to use for the health check. Defaults to `SPY`. |
| `pack_id` | string | The ID of the pack to use for the health check. Defaults to `zerosigma`. |
| `model_id` | string | The ID of the model to use for the health check. |

*   **Example Request**:

```
GET /healthz?ticker=AAPL
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the platform is healthy. |
| `checks` | object | An object containing the results of the health checks. |
| `errors` | object | An object containing any errors that occurred during the health checks. |

*   **Example Response**:

```json
{
  "ok": true,
  "checks": {
    "routers": {
      "models": true,
      "backtest": true,
      "admin": true,
      "audit": true,
      "calibration": true,
      "datasets": true,
      "health": true,
      "indicators": true,
      "leaderboard": true,
      "model_cards": true,
      "options": true,
      "packs": true,
      "policy": true,
      "runs": true,
      "signals": true,
      "sweep": true,
      "training": true
    },
    "indicators_count": 90,
    "polygon_api_key": true,
    "daily_bars_rows": 3,
    "hourly_bars_rows": 24,
    "snapshot_rows": 1000,
    "snapshot_has_iv": true,
    "db_ok": true
  },
  "errors": {}
}
```

## Indicators Router

The Indicators router provides endpoints for getting information about the technical indicators available in the platform.

### Get all indicators

*   **Endpoint**: `GET /indicators`
*   **Description**: This endpoint returns a list of all available technical indicators. You can optionally group the indicators by category.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `group` | boolean | Whether to group the indicators by category. Defaults to `false`. |
| `bypass_cache` | boolean | Whether to bypass the cache and fetch the latest data. Defaults to `false`. |

*   **Example Request**:

```
GET /indicators?group=true
```

*   **Response (group=false)**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `indicators` | array | An array of indicator objects. |

*   **Example Response (group=false)**:

```json
{
  "ok": true,
  "indicators": [
    {
      "name": "rsi",
      "category": "momentum",
      "subcategory": "general",
      "params": [
        "period"
      ],
      "doc": "Relative Strength Index"
    }
  ]
}
```

*   **Response (group=true)**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `groups` | object | An object containing the indicators grouped by category and subcategory. |

*   **Example Response (group=true)**:

```json
{
  "ok": true,
  "groups": {
    "momentum": {
      "general": [
        "rsi"
      ]
    }
  }
}
```

### Get indicator status

*   **Endpoint**: `GET /indicators/status`
*   **Description**: This endpoint returns the status of the indicators, including the total count and any load errors.
*   **Example Request**:

```
GET /indicators/status
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `count` | integer | The total number of indicators. |
| `load_errors` | array | An array of any errors that occurred while loading the indicators. |

*   **Example Response**:

```json
{
  "ok": true,
  "count": 90,
  "load_errors": []
}
```

## Leaderboard Router

The Leaderboard router provides endpoints for getting the leaderboard of top-performing models.

### Get the leaderboard

*   **Endpoint**: `GET /leaderboard`
*   **Description**: This endpoint returns a leaderboard of the top-performing models.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack to filter by. |
| `model_id` | string | The ID of the model to filter by. |
| `limit` | integer | The maximum number of results to return. Defaults to `20`. |
| `offset` | integer | The number of results to skip. Defaults to `0`. |
| `order_by` | string | The metric to order the results by. Can be `sharpe` or `cum_ret`. Defaults to `sharpe`. |

*   **Example Request**:

```
GET /leaderboard?pack_id=zerosigma&limit=10
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `rows` | array | An array of leaderboard objects. |
| `limit` | integer | The maximum number of results returned. |
| `offset` | integer | The number of results skipped. |
| `next_offset` | integer | The offset to use for the next page of results. |
| `order_by` | string | The metric the results are ordered by. |

*   **Example Response**:

```json
{
  "ok": true,
  "rows": [
    {
      "id": 1,
      "pack_id": "zerosigma",
      "model_id": "spy_opt_0dte_hourly",
      "best_sharpe_hourly": 1.2,
      "best_cum_ret": 0.12,
      "tag": "my_backtest"
    }
  ],
  "limit": 10,
  "offset": 0,
  "next_offset": 1,
  "order_by": "sharpe_hourly"
}
```

## Options Router

The Options router provides endpoints for working with options contracts.

### Create an options overlay

*   **Endpoint**: `POST /options_overlay`
*   **Description**: This endpoint allows you to create an options overlay for a given set of signals.
*   **Request Body**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to create the overlay for. |
| `pack_id` | string | The ID of the pack the model belongs to. Defaults to `swingsigma`. |
| `date` | string | The date to create the overlay for in `YYYY-MM-DD` format. Defaults to the current date. |
| `expiry` | string | The expiration date for the options in `YYYY-MM-DD` format. |
| `dte_target` | integer | The target number of days to expiration. |
| `option_mode` | string | The type of options to use. Can be `single` or `vertical`. Defaults to `single`. |
| `spread_width` | float | The width of the spread for vertical options. Defaults to `5.0`. |
| `side_override` | string | Whether to override the side of the trade. Can be `call` or `put`. |
| `target_delta` | float | The target delta for the options. Defaults to `0.35`. |
| `min_oi` | integer | The minimum open interest for the options. Defaults to `0`. |
| `limit` | integer | The maximum number of signals to process. Defaults to `100`. |
| `include_underlying_parity` | boolean | Whether to include a parity check for the underlying asset. Defaults to `true`. |
| `include_premium_parity` | boolean | Whether to include a parity check for the option premium. Defaults to `true`. |
| `write_parity_csv` | boolean | Whether to write the parity check results to a CSV file. Defaults to `false`. |

*   **Example Request**:

```json
{
  "model_id": "spy_eq_swing_daily",
  "date": "2024-01-01",
  "dte_target": 30
}
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `count` | integer | The number of overlays created. |
| `written` | integer | The number of overlays written to the database or CSV file. |
| `date` | string | The date the overlay was created for. |
| `expiry` | string | The expiration date of the options. |
| `parity` | object | An object containing the results of the underlying parity check. |
| `parity_premium` | object | An object containing the results of the premium parity check. |
| `parity_csv` | string | The path to the parity check CSV file. |

*   **Example Response**:

```json
{
  "ok": true,
  "count": 1,
  "written": 1,
  "date": "2024-01-01",
  "expiry": "2024-01-31",
  "parity": {
    "ok": true,
    "trades": 1,
    "hit_rate": 1
  },
  "parity_premium": {
    "ok": true,
    "trades": 1,
    "hit_rate_target": 1,
    "hit_rate_stop": 0,
    "timeouts": 0
  },
  "parity_csv": "reports/options_parity_2024-01-01_2024-01-31.csv"
}
```

### Get option signals

*   **Endpoint**: `GET /option_signals`
*   **Description**: This endpoint returns a list of option signals.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to filter by. |
| `pack_id` | string | The ID of the pack to filter by. |
| `date` | string | The date to filter by in `YYYY-MM-DD` format. |
| `start` | string | The start date for the signals in `YYYY-MM-DD` format. |
| `end` | string | The end date for the signals in `YYYY-MM-DD` format. |
| `tickers` | string | A comma-separated list of tickers to filter by. |
| `expiry` | string | The expiration date to filter by in `YYYY-MM-DD` format. |
| `occ_symbol` | string | The OCC symbol to filter by. |
| `limit` | integer | The maximum number of results to return. Defaults to `200`. |
| `offset` | integer | The number of results to skip. Defaults to `0`. |

*   **Example Request**:

```
GET /option_signals?model_id=spy_eq_swing_daily&limit=10
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `rows` | array | An array of option signal objects. |
| `count` | integer | The number of option signals returned. |
| `limit` | integer | The maximum number of results returned. |
| `offset` | integer | The number of results skipped. |
| `next_offset` | integer | The offset to use for the next page of results. |

*   **Example Response**:

```json
{
  "ok": true,
  "rows": [
    {
      "id": 1,
      "signal_id": 1,
      "occ_symbol": "O:SPY240119C00470000",
      "expiry": "2024-01-19",
      "strike": 470,
      "type": "call",
      "entry_premium_est": 1.23
    }
  ],
  "count": 1,
  "limit": 10,
  "offset": 0,
  "next_offset": 1
}
```

### List expirations

*   **Endpoint**: `GET /options/expirations`
*   **Description**: This endpoint returns a list of upcoming option expiration dates for a given ticker.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `ticker` | string | The ticker symbol to get the expirations for. |
| `start` | string | The start date to search from in `YYYY-MM-DD` format. Defaults to the current date. |
| `weeks` | integer | The number of weeks to search for expirations. Defaults to `12`. |

*   **Example Request**:

```
GET /options/expirations?ticker=SPY
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `ticker` | string | The ticker symbol that was searched for. |
| `start` | string | The start date that was used for the search. |
| `weeks` | integer | The number of weeks that were searched. |
| `expirations` | array | An array of expiration objects. |

*   **Example Response**:

```json
{
  "ok": true,
  "ticker": "SPY",
  "start": "2025-08-21",
  "weeks": 12,
  "expirations": [
    {
      "date": "2025-08-22",
      "has_chain": true,
      "count": 1000
    }
  ]
}
```

## Packs Router

The Packs router provides endpoints for getting information about packs.

### Get all packs

*   **Endpoint**: `GET /packs`
*   **Description**: This endpoint returns a list of all available packs.
*   **Example Request**:

```
GET /packs
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `packs` | array | An array of pack objects. |

*   **Example Response**:

```json
{
  "ok": true,
  "packs": [
    {
      "id": "zerosigma",
      "meta": {
        "name": "Zero Sigma",
        "description": "A pack for 0DTE options trading."
      }
    }
  ]
}
```

### Get a pack

*   **Endpoint**: `GET /packs/{pack_id}`
*   **Description**: This endpoint returns a single pack.
*   **Path Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack to get. |

*   **Example Request**:

```
GET /packs/zerosigma
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `pack` | object | The pack object. |

*   **Example Response**:

```json
{
  "ok": true,
  "pack": {
    "id": "zerosigma",
    "meta": {
      "name": "Zero Sigma",
      "description": "A pack for 0DTE options trading."
    },
    "indicator_sets": [
      {
        "name": "my_indicator_set"
      }
    ],
    "templates": [
      {
        "template_id": "0dte_hourly_options",
        "name": "0DTE Hourly Options",
        "template_version": 1
      }
    ],
    "models": [
      "spy_opt_0dte_hourly"
    ]
  }
}
```

### Get all templates for a pack

*   **Endpoint**: `GET /packs/{pack_id}/templates`
*   **Description**: This endpoint returns a list of all model templates for a given pack.
*   **Path Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack to get the templates for. |

*   **Example Request**:

```
GET /packs/zerosigma/templates
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `templates` | array | An array of template objects. |

*   **Example Response**:

```json
{
  "ok": true,
  "templates": [
    {
      "template_id": "0dte_hourly_options",
      "name": "0DTE Hourly Options",
      "pack": "zerosigma",
      "horizon": "0dte",
      "cadence": "hourly",
      "template_version": 1
    }
  ]
}
```

### Get all indicator sets for a pack

*   **Endpoint**: `GET /packs/{pack_id}/indicator_sets`
*   **Description**: This endpoint returns a list of all indicator sets for a given pack.
*   **Path Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack to get the indicator sets for. |

*   **Example Request**:

```
GET /packs/zerosigma/indicator_sets
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `indicator_sets` | array | An array of indicator set objects. |

*   **Example Response**:

```json
{
  "ok": true,
  "indicator_sets": [
    {
      "name": "my_indicator_set"
    }
  ]
}
```

## Policy Router

The Policy router provides endpoints for explaining and validating policies.

### Explain a policy

*   **Endpoint**: `GET /policy/explain`
*   **Description**: This endpoint returns an explanation of a policy, including the effective execution parameters and any validation checks.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to explain the policy for. |
| `pack_id` | string | The ID of the pack the model belongs to. Defaults to `zerosigma`. |

*   **Example Request**:

```
GET /policy/explain?model_id=spy_opt_0dte_hourly
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the policy is valid. |
| `schema_ok` | boolean | Indicates whether the policy schema is valid. |
| `schema_errors` | array | An array of any schema errors. |
| `execution_effective` | object | An object containing the effective execution parameters. |
| `checks` | object | An object containing the results of any validation checks. |

*   **Example Response**:

```json
{
  "ok": true,
  "schema_ok": true,
  "schema_errors": [],
  "execution_effective": {
    "slippage_bps": 1,
    "size_by_conf": false,
    "conf_cap": 1,
    "momentum_gate": false,
    "momentum_min": 0,
    "momentum_column": "momentum_score_total",
    "brackets": {
      "enabled": true,
      "mode": "atr",
      "entry_mode": "next_session_open",
      "atr_period": 14,
      "atr_mult_stop": 1.5,
      "atr_mult_target": 3,
      "time_stop_minutes": 120,
      "min_rr": 1,
      "regime_adjust": false
    },
    "options": {
      "selection": {
        "target_delta": 0.35,
        "dte_target": null,
        "min_oi": 0,
        "min_vol": null,
        "spread_width": 5,
        "weekly_ok": true
      }
    }
  },
  "checks": {
    "ok": true,
    "errors": [],
    "warnings": []
  }
}
```

## Runs Router

The Runs router provides endpoints for getting information about build runs, training runs, and sweeps.

### Get all build runs

*   **Endpoint**: `GET /build_runs`
*   **Description**: This endpoint returns a list of all build runs.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack to filter by. |
| `model_id` | string | The ID of the model to filter by. |
| `tag` | string | The tag to filter by. |
| `start` | string | The start date to filter by in `YYYY-MM-DD` format. |
| `end` | string | The end date to filter by in `YYYY-MM-DD` format. |
| `limit` | integer | The maximum number of results to return. Defaults to `20`. |
| `offset` | integer | The number of results to skip. Defaults to `0`. |

*   **Example Request**:

```
GET /build_runs?pack_id=zerosigma&limit=10
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `rows` | array | An array of build run objects. |
| `limit` | integer | The maximum number of results returned. |
| `offset` | integer | The number of results skipped. |
| `next_offset` | integer | The offset to use for the next page of results. |

*   **Example Response**:

```json
{
  "ok": true,
  "rows": [
    {
      "id": 1,
      "pack_id": "zerosigma",
      "model_id": "spy_opt_0dte_hourly",
      "started_at": "2025-08-21T12:00:00Z",
      "finished_at": "2025-08-21T12:01:00Z",
      "params": {},
      "metrics": {},
      "out_csv_uri": "matrices/spy_opt_0dte_hourly/training_matrix_built.csv",
      "lineage": {},
      "created_at": "2025-08-21T12:01:00Z"
    }
  ],
  "limit": 10,
  "offset": 0,
  "next_offset": 1
}
```

### Get all training runs

*   **Endpoint**: `GET /training_runs`
*   **Description**: This endpoint returns a list of all training runs.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack to filter by. |
| `model_id` | string | The ID of the model to filter by. |
| `tag` | string | The tag to filter by. |
| `start` | string | The start date to filter by in `YYYY-MM-DD` format. |
| `end` | string | The end date to filter by in `YYYY-MM-DD` format. |
| `limit` | integer | The maximum number of results to return. Defaults to `20`. |
| `offset` | integer | The number of results to skip. Defaults to `0`. |

*   **Example Request**:

```
GET /training_runs?pack_id=zerosigma&limit=10
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `rows` | array | An array of training run objects. |
| `limit` | integer | The maximum number of results returned. |
| `offset` | integer | The number of results skipped. |
| `next_offset` | integer | The offset to use for the next page of results. |

*   **Example Response**:

```json
{
  "ok": true,
  "rows": [
    {
      "id": 1,
      "pack_id": "zerosigma",
      "model_id": "spy_opt_0dte_hourly",
      "started_at": "2025-08-21T12:01:00Z",
      "finished_at": "2025-08-21T12:02:00Z",
      "params": {},
      "metrics": {},
      "model_out_uri": "artifacts/spy_opt_0dte_hourly/model.joblib",
      "features": [],
      "lineage": {},
      "created_at": "2025-08-21T12:02:00Z"
    }
  ],
  "limit": 10,
  "offset": 0,
  "next_offset": 1
}
```

### Get all sweeps

*   **Endpoint**: `GET /sweeps`
*   **Description**: This endpoint returns a list of all sweeps.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack to filter by. |
| `model_id` | string | The ID of the model to filter by. |
| `tag` | string | The tag to filter by. |
| `status` | string | The status to filter by. |
| `limit` | integer | The maximum number of results to return. Defaults to `20`. |
| `offset` | integer | The number of results to skip. Defaults to `0`. |

*   **Example Request**:

```
GET /sweeps?pack_id=zerosigma&limit=10
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `rows` | array | An array of sweep objects. |
| `limit` | integer | The maximum number of results returned. |
| `offset` | integer | The number of results skipped. |
| `next_offset` | integer | The offset to use for the next page of results. |

*   **Example Response**:

```json
{
  "ok": true,
  "rows": [
    {
      "id": 1,
      "pack_id": "zerosigma",
      "model_id": "spy_opt_0dte_hourly",
      "tag": "my_sweep",
      "status": "completed",
      "spec": {},
      "started_at": "2025-08-21T12:02:00Z",
      "finished_at": "2025-08-21T12:03:00Z",
      "created_at": "2025-08-21T12:03:00Z"
    }
  ],
  "limit": 10,
  "offset": 0,
  "next_offset": 1
}
```

### Get a sweep

*   **Endpoint**: `GET /sweeps/{sweep_id}`
*   **Description**: This endpoint returns a single sweep.
*   **Path Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `sweep_id` | integer | The ID of the sweep to get. |

*   **Example Request**:

```
GET /sweeps/1
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `sweep` | object | The sweep object. |
| `results` | array | An array of sweep result objects. |

*   **Example Response**:

```json
{
  "ok": true,
  "results": [
    {
      "id": 1,
      "kind": "backtest",
      "params": {},
      "metrics": {},
      "csv_uri": "sweeps/1/results.csv",
      "backtest_run_id": 1,
      "created_at": "2025-08-21T12:03:00Z"
    }
  ]
}
```

## Sweep Router

The Sweep router provides endpoints for running backtest sweeps.

### Run a backtest sweep

*   **Endpoint**: `POST /backtest_sweep`
*   **Description**: This endpoint allows you to run a backtest sweep for a given model.
*   **Request Body**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to run the sweep for. |
| `pack_id` | string | The ID of the pack the model belongs to. Defaults to `zerosigma`. |
| `start` | string | The start date for the sweep in `YYYY-MM-DD` format. |
| `end` | string | The end date for the sweep in `YYYY-MM-DD` format. |
| `thresholds_variants` | array | An array of comma-separated strings representing the prediction thresholds to test. |
| `allowed_hours_variants` | array | An array of comma-separated strings representing the allowed hours to test. |
| `top_pct_variants` | array | An array of floats representing the top prediction percentages to test. |
| `splits` | integer | The number of splits to use for cross-validation. Defaults to `5`. |
| `embargo` | float | The embargo percentage to use for cross-validation. Defaults to `0.0`. |
| `allowed_hours` | string | A comma-separated string of integers representing the hours of the day to allow trading. |
| `save` | boolean | Whether to save the sweep results to the database. Defaults to `true`. |
| `tag` | string | An optional tag to associate with the sweep. Defaults to `sweep`. |
| `min_trades` | integer | The minimum number of trades required for a result to be considered valid. Defaults to `0`. |
| `min_sharpe` | float | The minimum Sharpe ratio required for a result to be considered valid. |

*   **Example Request**:

```json
{
  "model_id": "spy_opt_0dte_hourly",
  "thresholds_variants": [
    "0.55,0.60,0.65",
    "0.60,0.65,0.70"
  ],
  "allowed_hours_variants": [
    "13,14,15"
  ]
}
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `runs` | array | An array of sweep run objects. |
| `count` | integer | The total number of runs in the sweep. |
| `filtered` | integer | The number of runs that passed the guardrails. |
| `report_path` | string | The path to the sweep report file. |
| `sweep_id` | integer | The ID of the sweep. |

*   **Example Response**:

```json
{
  "ok": true,
  "runs": [
    {
      "kind": "thresholds",
      "thresholds": "0.55,0.60,0.65",
      "allowed_hours": "13,14,15",
      "result": {
        "best_sharpe_hourly": 1.2,
        "best_cum_ret": 0.12,
        "total_trades": 100,
        "parity": null
      }
    }
  ],
  "count": 2,
  "filtered": 1,
  "report_path": "reports/backtest_sweep_spy_opt_0dte_hourly_20250821_120400.json",
  "sweep_id": 1
}
```

## Training Router

The Training router provides endpoints for training trading models.

### Train a model

*   **Endpoint**: `POST /train`
*   **Description**: This endpoint allows you to train a trading model.
*   **Request Body**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to train. |
| `csv` | string | The path to the training matrix CSV file. If not provided, the default training matrix for the model will be used. |
| `allowed_hours` | string or array | A comma-separated string or an array of integers representing the hours of the day to allow trading. |
| `calibration` | string | The type of calibration to use for the predictions. Can be `none`, `sigmoid`, or `isotonic`. Defaults to `sigmoid`. |
| `model_out` | string | The path to save the trained model to. If not provided, a default path will be used. |
| `target` | string | The name of the target column in the training matrix. |
| `pack_id` | string | The ID of the pack the model belongs to. Defaults to `zerosigma`. |

*   **Example Request**:

```json
{
  "model_id": "spy_opt_0dte_hourly"
}
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `model_out` | string | The path to the trained model. |
| `rows` | integer | The number of rows used for training. |

*   **Example Response**:

```json
{
  "ok": true,
  "model_out": "artifacts/spy_opt_0dte_hourly/gbm.pkl",
  "rows": 1000
}
```

## Signals Router

The Signals router provides endpoints for getting information about trading signals.

### Get all signals

*   **Endpoint**: `GET /signals`
*   **Description**: This endpoint returns a list of all trading signals.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to filter by. |
| `pack_id` | string | The ID of the pack to filter by. |
| `date` | string | The date to filter by in `YYYY-MM-DD` format. |
| `start` | string | The start date to filter by in `YYYY-MM-DD` format. |
| `end` | string | The end date to filter by in `YYYY-MM-DD` format. |
| `tickers` | string | A comma-separated list of tickers to filter by. |
| `limit` | integer | The maximum number of results to return. Defaults to `200`. |
| `offset` | integer | The number of results to skip. Defaults to `0`. |

*   **Example Request**:

```
GET /signals?model_id=spy_opt_0dte_hourly&limit=10
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `count` | integer | The number of signals returned. |
| `rows` | array | An array of signal objects. |
| `limit` | integer | The maximum number of results returned. |
| `offset` | integer | The number of results skipped. |
| `next_offset` | integer | The offset to use for the next page of results. |

*   **Example Response**:

```json
{
  "ok": true,
  "count": 1,
  "rows": [
    {
      "id": 1,
      "model_id": "spy_opt_0dte_hourly",
      "ticker": "SPY",
      "side": "buy",
      "entry_ref_px": 470.12,
      "close": 470.12,
      "stop_px": 465.42,
      "target_px": 474.82
    }
  ],
  "limit": 10,
  "offset": 0,
  "next_offset": 1
}
```

### Get signals summary

*   **Endpoint**: `GET /signals/summary`
*   **Description**: This endpoint returns a summary of live signals for a given model and period.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to get the summary for. |
| `risk_profile` | string | The risk profile to use for the summary. |
| `start` | string | The start date for the summary in `YYYY-MM-DD` format. |
| `end` | string | The end date for the summary in `YYYY-MM-DD` format. |

*   **Example Request**:

```
GET /signals/summary?model_id=spy_opt_0dte_hourly
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `model_id` | string | The ID of the model the summary is for. |
| `risk_profile` | string | The risk profile that was used for the summary. |
| `period` | object | An object containing the start and end dates of the summary. |
| `metrics` | object | An object containing the summary metrics. |

*   **Example Response**:

```json
{
  "ok": true,
  "model_id": "spy_opt_0dte_hourly",
  "risk_profile": "balanced",
  "period": {
    "start": null,
    "end": null
  },
  "metrics": {
    "sharpe": 1.2,
    "sortino": 1.5,
    "cum_return": 0.12,
    "win_rate": 0.6,
    "trades": 100,
    "fill_rate": 0.9,
    "avg_slippage": 0.01,
    "max_dd": 0.05,
    "coverage_pct": 1,
    "freshness_sec": 3600
  }
}
```

### Get signals leaderboard

*   **Endpoint**: `GET /signals/leaderboard`
*   **Description**: This endpoint returns a leaderboard of the top-performing models based on their live signals.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack` | string | The ID of the pack to filter by. |
| `risk_profile` | string | The risk profile to use for the leaderboard. |
| `start` | string | The start date for the leaderboard in `YYYY-MM-DD` format. |
| `end` | string | The end date for the leaderboard in `YYYY-MM-DD` format. |
| `limit` | integer | The maximum number of results to return. Defaults to `50`. |
| `offset` | integer | The number of results to skip. Defaults to `0`. |

*   **Example Request**:

```
GET /signals/leaderboard?pack=zerosigma&limit=10
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `rows` | array | An array of leaderboard objects. |
| `total` | integer | The total number of models on the leaderboard. |

*   **Example Response**:

```json
{
  "ok": true,
  "rows": [
    {
      "model_id": "spy_opt_0dte_hourly",
      "risk_profile": "balanced",
      "period": {
        "start": null,
        "end": null
      },
      "metrics": {
        "sharpe": 1.2,
        "sortino": 1.5,
        "cum_return": 0.12,
        "win_rate": 0.6,
        "trades": 100,
        "fill_rate": 0.9,
        "avg_slippage": 0.01,
        "capacity": 1000000,
        "coverage_pct": 1,
        "freshness_sec": 3600
      },
      "lineage": {}
    }
  ],
  "total": 1
}
```

### Get model performance

*   **Endpoint**: `GET /models/{model_id}/performance`
*   **Description**: This endpoint returns a summary of a model's live and backtest performance.
*   **Path Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to get the performance for. |

*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `risk_profile` | string | The risk profile to use for the performance summary. |
| `start` | string | The start date for the performance summary in `YYYY-MM-DD` format. |
| `end` | string | The end date for the performance summary in `YYYY-MM-DD` format. |

*   **Example Request**:

```
GET /models/spy_opt_0dte_hourly/performance
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `live` | object | An object containing the live performance metrics. |
| `backtest` | object | An object containing the backtest performance metrics. |

*   **Example Response**:

```json
{
  "ok": true,
  "live": {
    "period": {
      "start": null,
      "end": null
    },
    "metrics": {
      "sharpe": 1.2,
      "sortino": 1.5,
      "cum_return": 0.12,
      "win_rate": 0.6,
      "trades": 100,
      "fill_rate": 0.9,
      "avg_slippage": 0.01,
      "max_dd": 0.05,
      "coverage_pct": 1,
      "freshness_sec": 3600
    }
  },
  "backtest": {
    "started_at": "2025-08-21T12:02:00Z",
    "metrics": {
      "best_sharpe_hourly": 1.2,
      "best_cum_ret": 0.12
    }
  }
}
```

### Validate a policy

*   **Endpoint**: `GET /validate_policy`
*   **Description**: This endpoint is a compatibility alias for `GET /policy/explain`.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `model_id` | string | The ID of the model to validate the policy for. |
| `pack_id` | string | The ID of the pack the model belongs to. Defaults to `zerosigma`. |

*   **Example Request**:

```
GET /validate_policy?model_id=spy_opt_0dte_hourly
```

*   **Response**: See the response for `GET /policy/explain`.

## Model Cards Router

The Model Cards router provides endpoints for getting information about model cards.

### Get all model cards for a model

*   **Endpoint**: `GET /model_cards`
*   **Description**: This endpoint returns a list of all model cards for a given model.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack the model belongs to. Defaults to `zerosigma`. |
| `model_id` | string | The ID of the model to get the model cards for. |
| `limit` | integer | The maximum number of results to return. Defaults to `200`. |
| `offset` | integer | The number of results to skip. Defaults to `0`. |

*   **Example Request**:

```
GET /model_cards?model_id=spy_opt_0dte_hourly
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**:

| Name | Type | Description |
| --- | --- | --- |
| `ok` | boolean | Indicates whether the request was successful. |
| `count` | integer | The number of model cards returned. |
| `cards` | array | An array of model card objects. |
| `limit` | integer | The maximum number of results returned. |
| `offset` | integer | The number of results skipped. |
| `next_offset` | integer | The offset to use for the next page of results. |

*   **Example Response**:

```json
{
  "ok": true,
  "count": 1,
  "cards": [
    {
      "pack_id": "zerosigma",
      "model_id": "spy_opt_0dte_hourly",
      "event": "backtest",
      "created_at": "2025-08-21T12:00:00Z"
    }
  ],
  "limit": 200,
  "offset": 0,
  "next_offset": 1
}
```

### Get a model card

*   **Endpoint**: `GET /model_card`
*   **Description**: This endpoint returns a single model card.
*   **Query Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `pack_id` | string | The ID of the pack the model belongs to. Defaults to `zerosigma`. |
| `model_id` | string | The ID of the model to get the model card for. |
| `file` | string | The name of the model card file to get. If not provided, the latest model card will be returned. |

*   **Example Request**:

```
GET /model_card?model_id=spy_opt_0dte_hourly
```

*   **Response**:

    *   **Status Code**: `200 OK`
    *   **Body**: The body of the response will be the content of the model card file in JSON format.

*   **Example Response**:

```json
{
  "ok": true,
  "pack_id": "zerosigma",
  "model_id": "spy_opt_0dte_hourly",
  "event": "backtest",
  "created_at": "2025-08-21T12:00:00Z",
  "params": {
    "thresholds": [
      0.55,
      0.6,
      0.65
    ]
  },
  "metrics": {
    "best_sharpe_hourly": 1.2
  }
}
```
