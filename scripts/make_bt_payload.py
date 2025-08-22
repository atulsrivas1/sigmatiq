#!/usr/bin/env python
import os
import json
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="bt_payload.json")
    args = ap.parse_args()

    payload = {
        "model_id": os.environ.get("MODEL_ID"),
        "pack_id": os.environ.get("PACK_ID", "zerosigma"),
        "splits": int(os.environ.get("SPLITS", "5") or 5),
    }
    tgt = os.environ.get("TARGET")
    if tgt:
        payload["target"] = tgt
    hrs = os.environ.get("ALLOWED_HOURS")
    if hrs:
        payload["allowed_hours"] = hrs
    top = os.environ.get("TOP_PCT")
    if top:
        try:
            payload["top_pct"] = float(top)
        except Exception:
            payload["top_pct"] = top
    else:
        payload["thresholds"] = os.environ.get("THRESHOLDS", "0.55,0.60,0.65")

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    print(f"WROTE {args.out}")


if __name__ == "__main__":
    main()

