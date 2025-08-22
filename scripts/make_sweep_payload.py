#!/usr/bin/env python
import os, json, argparse


def _split_csvfloats(s):
    vals = []
    for x in (s or '').split(','):
        x = x.strip()
        if not x:
            continue
        try:
            vals.append(float(x))
        except Exception:
            pass
    return vals


def _split_semicolon_csv(s):
    # "13,14,15;9,10,11,12,13,14,15,16" -> ["13,14,15", "9,10,11,12,13,14,15,16"]
    out = []
    for part in (s or '').split(';'):
        part = part.strip()
        if part:
            out.append(part)
    return out


def _split_threshold_variants(s):
    # "0.50,0.55;0.60,0.65" -> ["0.50,0.55", "0.60,0.65"]
    return _split_semicolon_csv(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='sweep_payload.json')
    args = ap.parse_args()

    payload = {
        'model_id': os.environ.get('MODEL_ID'),
        'pack_id': os.environ.get('PACK_ID', 'zerosigma'),
        'splits': int(os.environ.get('SPLITS', '5') or 5),
        'embargo': float(os.environ.get('EMBARGO', '0') or 0.0),
        'save': True,
        'tag': os.environ.get('TAG', 'sweep'),
    }

    # Threshold variants (optional)
    thr_variants_env = os.environ.get('THR_VARIANTS') or os.environ.get('THRESHOLDS_VARIANTS')
    if thr_variants_env:
        payload['thresholds_variants'] = _split_threshold_variants(thr_variants_env)

    # Top % variants (optional)
    top_csv = os.environ.get('TOP_PCTS') or os.environ.get('TOP_PCT_VARIANTS')
    if top_csv:
        payload['top_pct_variants'] = _split_csvfloats(top_csv)

    # Hours variants (semicolon-delimited CSVs)
    hours_sets = os.environ.get('HOURS_SETS') or os.environ.get('ALLOWED_HOURS_VARIANTS')
    if hours_sets:
        payload['allowed_hours_variants'] = _split_semicolon_csv(hours_sets)
    else:
        # Fallback to a single ALLOWED_HOURS string if provided
        ah = os.environ.get('ALLOWED_HOURS')
        if ah:
            payload['allowed_hours_variants'] = [ah]

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(payload, f)
    print(f'WROTE {args.out}')


if __name__ == '__main__':
    main()

