import sys
from pathlib import Path
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _get_app():
    import importlib
    spec = importlib.util.spec_from_file_location("sigma_api_app", ROOT / "api" / "app.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return getattr(module, "app")


def test_build_matrix_date_validation():
    app = _get_app()
    client = TestClient(app)
    payload = {
        "model_id": "m",
        "start": "2025/01/01",  # bad format
        "end": "2025-01-02"
    }
    r = client.post("/build_matrix", json=payload)
    assert r.status_code in (400, 422)

