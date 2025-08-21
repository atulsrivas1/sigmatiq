# Data Models

This document describes the data models used throughout the Sigmatiq application.

## Registry Artifacts

These Pydantic models represent various artifacts stored in the registry.

### IndicatorSetVersion

*   **Class**: `IndicatorSetVersion(BaseModel)`
*   **Description**: This class represents a version of an indicator set.
*   **Attributes**:

| Name | Type | Description |
| --- | --- | --- |
| `id` | `int` | The ID of the indicator set version. |
| `name` | `str` | The name of the indicator set. |
| `version` | `str` | The version of the indicator set. |
| `description` | `str` | A description of the indicator set. |
| `created_at` | `datetime` | The creation timestamp. |
| `updated_at` | `datetime` | The last update timestamp. |

### IndicatorSpec

*   **Class**: `IndicatorSpec(BaseModel)`
*   **Description**: This class represents the specification of a single indicator within an indicator set.
*   **Attributes**:

| Name | Type | Description |
| --- | --- | --- |
| `id` | `int` | The ID of the indicator specification. |
| `indicator_set_id` | `int` | The ID of the indicator set this specification belongs to. |
| `name` | `str` | The name of the indicator. |
| `version` | `str` | The version of the indicator. |
| `params` | `Dict[str, Any]` | A dictionary of parameters for the indicator. |
| `created_at` | `datetime` | The creation timestamp. |
| `updated_at` | `datetime` | The last update timestamp. |

### ModelVersion

*   **Class**: `ModelVersion(BaseModel)`
*   **Description**: This class represents a version of a trained model.
*   **Attributes**:

| Name | Type | Description |
| --- | --- | --- |
| `id` | `int` | The ID of the model version. |
| `name` | `str` | The name of the model. |
| `version` | `str` | The version of the model. |
| `description` | `str` | A description of the model. |
| `artifact_uri` | `str` | The URI to the model artifact. |
| `data_hash` | `str` | The hash of the data used to train the model. |
| `git_sha` | `str` | The Git SHA of the codebase used to train the model. |
| `metrics` | `Dict[str, Any]` | A dictionary of metrics for the model. |
| `created_at` | `datetime` | The creation timestamp. |
| `updated_at` | `datetime` | The last update timestamp. |

### PolicyVersion

*   **Class**: `PolicyVersion(BaseModel)`
*   **Description**: This class represents a version of a policy.
*   **Attributes**:

| Name | Type | Description |
| --- | --- | --- |
| `id` | `int` | The ID of the policy version. |
| `name` | `str` | The name of the policy. |
| `version` | `str` | The version of the policy. |
| `description` | `str` | A description of the policy. |
| `spec` | `Dict[str, Any]` | The specification of the policy. |
| `created_at` | `datetime` | The creation timestamp. |
| `updated_at` | `datetime` | The last update timestamp. |

## Live Metrics

### LiveMetrics

*   **Class**: `LiveMetrics(dataclass)`
*   **Description**: This dataclass represents live performance metrics for a trading model.
*   **Attributes**:

| Name | Type | Description |
| --- | --- | --- |
| `sharpe` | `Optional[float]` | The Sharpe ratio. |
| `sortino` | `Optional[float]` | The Sortino ratio. |
| `cum_return` | `Optional[float]` | The cumulative return. |
| `win_rate` | `Optional[float]` | The win rate. |
| `trades` | `int` | The number of trades. |
| `max_dd` | `Optional[float]` | The maximum drawdown. |
| `fill_rate` | `Optional[float]` | The fill rate. |
| `avg_slippage` | `Optional[float]` | The average slippage. |
| `capacity` | `Optional[str]` | The capacity. |
| `coverage_pct` | `Optional[float]` | The coverage percentage. |
| `freshness_sec` | `Optional[int]` | The freshness in seconds. |
