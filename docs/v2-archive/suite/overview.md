# Sigma Product Suite Overview

The suite works like this:

```
Packs -> Build -> Backtest -> Leaderboard -> Train -> Alerts
```

- Packs hold strategy settings.
- Build creates clean historical data and features.
- Backtest scores performance.
- Leaderboard highlights the best runs.
- Train locks in a model for alerts.

Roles (high level)
- Analyst: chooses packs, runs builds and backtests, reads leaderboards.
- Operator: triggers sweeps and training, checks health.
- Admin: manages users, packs, and quotas.

Related reading
- [Start Here](../START_HERE.md)
- [Modeling Pipeline Guide](../MODELING_PIPELINE_GUIDE.md)
- [Packs](../products/packs.md)
