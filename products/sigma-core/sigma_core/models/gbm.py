import argparse
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from typing import List

from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

from ..cv.splits import PurgedEmbargoedWalkForwardSplit
from ..features.builder import select_features


def main():
    parser = argparse.ArgumentParser(description="Train XGBoost model for 0DTE hourly direction")
    parser.add_argument("--csv", type=str, default="train_sample.csv", help="Path to training CSV (matrix)")
    parser.add_argument("--target", type=str, default=None, help="Target column: y or y_syn (auto if not provided)")
    parser.add_argument("--model_out", type=str, default="models/gbm_0dte.pkl", help="Output path for model")
    parser.add_argument("--splits", type=int, default=3, help="Number of walk-forward splits")
    parser.add_argument("--allowed_hours", type=str, default=None, help="Comma-separated ET hours to include (e.g., 13,14,15)")
    args = parser.parse_args()

    df = pd.read_csv(args.csv)

    y_col = args.target
    if y_col is None:
        if "y" in df.columns and df["y"].notna().any():
            y_col = "y"
        elif "y_syn" in df.columns:
            y_col = "y_syn"
        else:
            raise ValueError("No target column found (expected 'y' or 'y_syn')")

    # Optional: filter by allowed hours
    if args.allowed_hours:
        try:
            allowed = {int(x) for x in args.allowed_hours.split(',') if x.strip() != ''}
            if 'hour_et' in df.columns and allowed:
                df = df[df['hour_et'].isin(allowed)]
        except Exception:
            pass

    # Drop rows with missing target
    df = df[df[y_col].notna()].reset_index(drop=True)

    # Derive timestamp for ordering (after filtering)
    if {"date", "hour_et"}.issubset(df.columns):
        ts = pd.to_datetime(df["date"]) + pd.to_timedelta(df["hour_et"], unit="h")
    else:
        ts = pd.Series(pd.date_range("2000-01-01", periods=len(df), freq="H"))

    X = df[select_features(df)].fillna(0.0).values
    y_raw = df[y_col].astype(str).values
    le = LabelEncoder(); y = le.fit_transform(y_raw)

    # Simple model train (no CV here; CV in backtest)
    model = XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.08, subsample=0.9, colsample_bytree=0.9, eval_metric="mlogloss", tree_method="hist", random_state=2025)
    model.fit(X, y)
    Path(args.model_out).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": select_features(df), "label_encoder": le}, args.model_out)
    print(f"Saved model to {args.model_out}")


if __name__ == "__main__":
    main()
