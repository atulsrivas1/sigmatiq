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


def test_indicators_status_endpoint():
    app = _get_app()
    client = TestClient(app)
    r = client.get("/indicators/status")
    assert r.status_code == 200
    data = r.json()
    assert data.get("ok") is True
    assert isinstance(data.get("count"), int)
    assert "load_errors" in data

