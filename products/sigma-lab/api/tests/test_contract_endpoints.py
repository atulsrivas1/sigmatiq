import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient


def _get_app():
    import importlib
    spec = importlib.util.spec_from_file_location("edge_api_app", ROOT / "edge_api" / "app.py")
    module = importlib.util.module_from_spec(spec)  # type: ignore
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore
    return getattr(module, "app")


def test_contract_indicators_shape():
    app = _get_app()
    client = TestClient(app)
    r = client.get("/indicators")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "ok" in data
    assert ("indicators" in data) or ("groups" in data) or (data.get("ok") in (True, False))


def test_contract_model_cards_list_shape():
    app = _get_app()
    client = TestClient(app)
    r = client.get("/model_cards?pack_id=zeroedge&model_id=nonexistent_model&limit=3&offset=0")
    assert r.status_code == 200
    data = r.json()
    assert data.get("ok") is True
    assert "cards" in data and isinstance(data["cards"], list)
    assert "limit" in data and "offset" in data and "next_offset" in data


def test_contract_leaderboard_shape():
    app = _get_app()
    client = TestClient(app)
    r = client.get("/leaderboard?limit=2&offset=0")
    assert r.status_code == 200
    data = r.json()
    assert "ok" in data
    # Either rows on success (DB present) or error on no DB
    assert ("rows" in data) or ("error" in data)


def test_contract_policy_explain_shape():
    app = _get_app()
    client = TestClient(app)
    r = client.get("/policy/explain?model_id=nonexistent_model&pack_id=zeroedge")
    assert r.status_code == 200
    data = r.json()
    assert "ok" in data
    assert "schema_ok" in data and "schema_errors" in data
    assert "execution_effective" in data and isinstance(data["execution_effective"], dict)
    assert "checks" in data and isinstance(data["checks"], dict)


def test_contract_option_signals_shape():
    app = _get_app()
    client = TestClient(app)
    r = client.get("/option_signals?limit=2&offset=0")
    assert r.status_code == 200
    data = r.json()
    assert "ok" in data
    assert "rows" in data and isinstance(data["rows"], list)
    assert "limit" in data and "offset" in data and "next_offset" in data


def test_contract_audit_shape():
    app = _get_app()
    client = TestClient(app)
    r = client.get("/audit?limit=1&offset=0")
    assert r.status_code == 200
    data = r.json()
    assert "ok" in data
    assert "rows" in data and isinstance(data["rows"], list)
    assert "limit" in data and "offset" in data and "next_offset" in data
