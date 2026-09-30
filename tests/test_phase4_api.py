from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_phase4_routes_registered():
    paths={r.path for r in app.routes}
    assert '/api/agents' in paths
    assert '/api/agents/run' in paths
    assert '/api/plugins' in paths
    assert '/api/plugins/execute' in paths
