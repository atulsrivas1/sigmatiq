import sys
from pathlib import Path
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _get_app():
    import importlib.util
    spec = importlib.util.spec_from_file_location("sigma_api_app", ROOT / "app.py")
    module = importlib.util.module_from_spec(spec)  # type: ignore
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore
    return getattr(module, "app")


def test_index_and_health():
    app = _get_app()
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200 and r.json().get('ok') is True
    r = client.get("/health")
    assert r.status_code == 200 and 'ok' in r.json()


def test_models_and_validate_policy_defaults():
    app = _get_app()
    client = TestClient(app)
    # Default list_models (zerosigma pack)
    r = client.get("/models")
    assert r.status_code == 200 and 'models' in r.json()
    # validate_policy should return error for missing policy when model not present
    r = client.get("/validate_policy", params={"model_id": "nonexistent", "pack_id": "zerosigma"})
    assert r.status_code in (200, 400)
    data = r.json()
    assert 'ok' in data
