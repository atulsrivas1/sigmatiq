#!/usr/bin/env python
import argparse
from pathlib import Path


def derive_model_id(args) -> str:
    parts = [
        (args.ticker or "").lower(),
        args.asset or "",
        args.horizon or "",
        args.cadence or "",
    ]
    if args.algo:
        parts.append(args.algo)
    if args.variant:
        parts.append(args.variant)
    return "_".join([p for p in parts if p])


def main():
    p = argparse.ArgumentParser(description="Scaffold a new model directory and policy template")
    p.add_argument("--pack_id", required=True)
    p.add_argument("--model_id")
    p.add_argument("--ticker")
    p.add_argument("--asset", help="opt|eq")
    p.add_argument("--horizon", help="0dte|intraday|swing|long")
    p.add_argument("--cadence", help="5m|15m|hourly|daily")
    p.add_argument("--algo")
    p.add_argument("--variant")
    args = p.parse_args()

    model_id = args.model_id or derive_model_id(args)
    if not model_id:
        raise SystemExit("model_id could not be derived; provide --model_id or auto fields")

    root = Path("models") / args.pack_id / model_id
    root.mkdir(parents=True, exist_ok=True)
    (root / "README.md").write_text(
        f"# {model_id}\n\nPack: {args.pack_id}\nTicker: {args.ticker or ''}\n",
        encoding="utf-8",
    )
    (root / "policy.yaml").write_text(
        (
            "pack_id: {pack}\n"
            "model_id: {mid}\n"
            "description: |\n  TODO: Describe the model.\n"
            "data:\n  ticker: {ticker}\n  cadence: {cadence}\n  horizon: {horizon}\n"
            "features:\n  sets: [baseline]\n"
            "labels:\n  name: hourly_direction\n"
            "train:\n  calibration: sigmoid\n"
            "backtest:\n  thresholds: [0.55, 0.60, 0.65]\n  splits: 5\n"
        ).format(
            pack=args.pack_id,
            mid=model_id,
            ticker=args.ticker or "",
            cadence=args.cadence or "",
            horizon=args.horizon or "",
        ),
        encoding="utf-8",
    )
    print(f"Scaffolded model at {root}")


if __name__ == "__main__":
    main()

