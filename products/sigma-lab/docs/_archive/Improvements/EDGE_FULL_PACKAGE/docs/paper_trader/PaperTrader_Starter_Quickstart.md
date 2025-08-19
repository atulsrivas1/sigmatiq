
# Paper Trader — Starter Assets (Quickstart)
*Generated: 2025-08-15 20:56 UTC*

**Files**
- Packs → paper defaults: `paper_account.yaml`, `fill_models.yaml` (for: zerosigma, swingsigma, longsigma, overnightsigma, momentumsigma)
- SwingSigma policy (brackets): `packs/swingsigma/policy_templates/universe_eq_swing_daily_scanner.yaml`
- CLI harness: `scripts/paper_run.py`

**Run**
```bash
python scripts/paper_run.py --create-account --account-name default_paper
python scripts/paper_run.py --pack-id swingsigma --model-id universe_eq_swing_daily_scanner   --signals scans/breakout_momentum/2025-08-15.csv --stream
```
