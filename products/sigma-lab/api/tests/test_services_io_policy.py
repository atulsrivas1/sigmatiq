from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.services.io import workspace_paths, resolve_indicator_set_path, PACKS_DIR
from api.services.policy import ensure_policy_exists, load_policy, validate_policy_file


def test_workspace_paths_and_indicator_resolution_tmp():
    model_id = 'unit_test_model'
    ws = workspace_paths(model_id, 'zerosigma')
    # Check expected keys and directories
    assert 'matrices' in ws and 'policy' in ws and 'config' in ws
    # Create a temporary indicator set for the model and ensure resolver picks it
    ind_dir = PACKS_DIR / 'zerosigma' / 'indicator_sets'
    ind_dir.mkdir(parents=True, exist_ok=True)
    ind_path = ind_dir / f'{model_id}.yaml'
    ind_path.write_text('features: []\n')
    p = resolve_indicator_set_path('zerosigma', model_id)
    assert p == ind_path


def test_policy_ensure_and_load_valid():
    model_id = 'unit_test_model_policy'
    pol_dir = PACKS_DIR / 'zerosigma' / 'policy_templates'
    pol_dir.mkdir(parents=True, exist_ok=True)
    pol_path = pol_dir / f'{model_id}.yaml'
    doc = {
        'policy': {
            'risk': { 'max_drawdown': 10, 'max_exposure': 100 },
            'execution': { 'slippage_bps': 1.0, 'size_by_conf': False, 'conf_cap': 1.0 },
            'alerting': { 'cooldown_minutes': 5 }
        }
    }
    pol_path.write_text(yaml.safe_dump(doc))
    err = ensure_policy_exists(model_id, 'zerosigma')
    assert err is None
    data = load_policy(model_id, 'zerosigma')
    assert isinstance(data, dict) and 'execution' in data and 'risk' in data
    ok, errs = validate_policy_file(pol_path)
    assert ok and not errs


def test_policy_invalid_schema_detected():
    model_id = 'unit_test_model_policy_bad'
    pol_path = PACKS_DIR / 'zerosigma' / 'policy_templates' / f'{model_id}.yaml'
    pol_path.parent.mkdir(parents=True, exist_ok=True)
    pol_path.write_text('policy: invalid')
    msg = ensure_policy_exists(model_id, 'zerosigma')
    assert isinstance(msg, str) and 'invalid' in msg

