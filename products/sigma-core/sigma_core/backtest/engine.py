import argparse
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import numpy as np
import pandas as pd

from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.calibration import CalibratedClassifierCV

from ..cv.splits import PurgedEmbargoedWalkForwardSplit
from ..features.builder import select_features
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _extract_dir_probs(y_proba: np.ndarray, classes: List[str]) -> Tuple[np.ndarray, np.ndarray]:
    c2i = {c: i for i, c in enumerate(classes)}
    p_up = y_proba[:, c2i.get("UP", 0)] if "UP" in c2i else np.zeros(len(y_proba))
    p_down = y_proba[:, c2i.get("DOWN", 1)] if "DOWN" in c2i else np.zeros(len(y_proba))
    return p_up, p_down


def _confidence_from_probs(p_up: np.ndarray, p_down: np.ndarray) -> np.ndarray:
    # Directional confidence vs the rest: conf = max(p_up, p_down) vs others
    p_dir = np.maximum(p_up, p_down)
    conf = np.maximum(0.0, 2.0 * p_dir - 1.0)  # scale so 0.5 -> 0.0, 1.0 -> 1.0
    return conf


def _positions_threshold(y_proba: np.ndarray, classes: List[str], proba_threshold: float, *, size_by_conf: bool = False, conf_cap: float = 1.0) -> np.ndarray:
    c2i = {c: i for i, c in enumerate(classes)}
    p_up = y_proba[:, c2i.get("UP", 0)] if "UP" in c2i else np.zeros(len(y_proba))
    p_down = y_proba[:, c2i.get("DOWN", 1)] if "DOWN" in c2i else np.zeros(len(y_proba))
    sign = np.where((p_up >= proba_threshold) & (p_up > p_down), 1,
                    np.where((p_down >= proba_threshold) & (p_down > p_up), -1, 0))
    if not size_by_conf:
        return sign.astype(float)
    conf = _confidence_from_probs(p_up, p_down)
    size = np.minimum(conf, conf_cap)
    return sign.astype(float) * size


def _positions_top_pct(y_proba: np.ndarray, classes: List[str], top_pct: float, *, size_by_conf: bool = False, conf_cap: float = 1.0) -> np.ndarray:
    c2i = {c: i for i, c in enumerate(classes)}
    p_up = y_proba[:, c2i.get("UP", 0)] if "UP" in c2i else np.zeros(len(y_proba))
    p_down = y_proba[:, c2i.get("DOWN", 1)] if "DOWN" in c2i else np.zeros(len(y_proba))
    conf = np.maximum(p_up, p_down)
    n = len(conf)
    k = max(1, int(np.floor(top_pct * n)))
    idx = np.argsort(-conf)[:k]
    pos = np.zeros(n, dtype=float)
    # Direction by larger of UP/DOWN
    sign = np.where(p_up[idx] >= p_down[idx], 1.0, -1.0)
    if not size_by_conf:
        pos[idx] = sign
        return pos
    conf_sel = _confidence_from_probs(p_up[idx], p_down[idx])
    size = np.minimum(conf_sel, conf_cap)
    pos[idx] = sign * size
    return pos


def run_backtest(
    df: pd.DataFrame,
    target_col: str,
    thresholds: List[float],
    *,
    splits: int = 5,
    embargo: float = 0.0,
    top_pct: Optional[float] = None,
    plots_dir: Optional[str] = None,
    allowed_hours: Optional[List[int]] = None,
    slippage_bps: float = 1.0,
    size_by_conf: bool = False,
    conf_cap: float = 1.0,
    per_hour_thresholds: bool = False,
    per_hour_select_by: str = 'sharpe',
    calibration: Optional[str] = 'sigmoid',
    momentum_gate: bool = False,
    momentum_min: float = 0.0,
    momentum_column: str = 'momentum_score_total',
    return_fold_outputs: bool = False,
) -> Dict[str, any]:
    if allowed_hours and 'hour_et' in df.columns:
        df = df[df['hour_et'].isin(allowed_hours)].copy()

    feat_cols = select_features(df)
    X = df[feat_cols].fillna(0.0).values
    y_raw = df[target_col].astype(str).values
    le = LabelEncoder(); y = le.fit_transform(y_raw)

    splitter = PurgedEmbargoedWalkForwardSplit(n_splits=splits, embargo=embargo)
    results = []
    cum_rets = []
    fold_outputs = []
    for fold, (train_idx, test_idx) in enumerate(splitter.split(X)):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        model = XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.08, subsample=0.9, colsample_bytree=0.9, eval_metric="mlogloss", tree_method="hist", random_state=2025)
        if calibration in {"sigmoid", "isotonic"}:
            try:
                clf = CalibratedClassifierCV(model, method=calibration, cv=3)
                clf.fit(X_train, y_train)
                final = clf
            except Exception:
                model.fit(X_train, y_train); final = model
        else:
            model.fit(X_train, y_train); final = model

        y_proba = final.predict_proba(X_test)
        classes = list(getattr(final, 'classes_', le.classes_))
        p_up, p_down = _extract_dir_probs(y_proba, classes)
        conf = _confidence_from_probs(p_up, p_down)
        if return_fold_outputs:
            fold_outputs.append({
                'fold': int(fold),
                'test_idx': test_idx.tolist(),
                'classes': classes,
                'y_proba': y_proba.tolist(),
            })

        if top_pct is not None and top_pct != "":
            pos = _positions_top_pct(y_proba, classes, float(top_pct), size_by_conf=size_by_conf, conf_cap=conf_cap)
            thr_used = None
        else:
            best = None
            for thr in thresholds:
                pos_thr = _positions_threshold(y_proba, classes, thr, size_by_conf=size_by_conf, conf_cap=conf_cap)
                # Simple return proxy: direction correctness
                ret = np.mean(np.where(((p_up >= thr) & (p_up > p_down) & (y_test == le.transform(['UP'])[0])) | ((p_down >= thr) & (p_down > p_up) & (y_test == le.transform(['DOWN'])[0])), 1.0, 0.0))
                if best is None or ret > best[0]:
                    best = (ret, thr, pos_thr)
            pos = best[2] if best else np.zeros_like(y_test, dtype=float)
            thr_used = best[1] if best else None

        # Momentum gate: zero out positions when momentum below threshold
        if momentum_gate and (momentum_column in df.columns):
            try:
                gate_vals = df.iloc[test_idx][momentum_column].astype(float).fillna(0.0).values
                gate = (gate_vals >= float(momentum_min)).astype(float)
                pos = pos * gate
            except Exception:
                pass

        # Simple PnL proxy with slippage
        pnl = pos * (np.where(y_test == le.transform(['UP'])[0], 1.0, np.where(y_test == le.transform(['DOWN'])[0], -1.0, 0.0)))
        pnl -= np.where(pos != 0, slippage_bps/10000.0, 0.0)
        cum_ret = float(np.sum(pnl))
        sharpe_hourly = float(np.mean(pnl) / (np.std(pnl) + 1e-9))
        results.append({"fold": fold, "thr": thr_used, "cum_ret": cum_ret, "sharpe_hourly": sharpe_hourly, "trades": int(np.sum(np.abs(pos)>0))})
        cum_rets.append(cum_ret)

    # Plot cumulative returns across folds if requested
    top_result = None
    if results:
        df_res = pd.DataFrame(results)
        if plots_dir:
            Path(plots_dir).mkdir(parents=True, exist_ok=True)
            plt.figure(figsize=(8,4))
            plt.plot(np.cumsum(df_res['cum_ret'].values), label='cum_ret')
            plt.title('Cumulative return across folds')
            plt.grid(True)
            out_png = Path(plots_dir) / 'cum_returns.png'
            plt.savefig(out_png)
        # Select best by sharpe
        best_idx = int(np.argmax(df_res['sharpe_hourly'].values))
        top_result = df_res.iloc[best_idx].to_dict()

    out = {"threshold_results": results, "top_pct_result": top_result}
    if return_fold_outputs:
        out["fold_outputs"] = fold_outputs
    return out
