import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient


def _get_app():
    # Import app from api
    import importlib
    spec = importlib.util.spec_from_file_location("sigma_api_app", ROOT / "app.py")
    module = importlib.util.module_from_spec(spec)  # type: ignore
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore
    return getattr(module, "app")


def test_indicators_endpoint():
    app = _get_app()
    client = TestClient(app)
    r = client.get("/indicators")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "indicators" in data or (data.get("ok") is False)


def test_health_endpoint_shape():
    app = _get_app()
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert "ok" in data
