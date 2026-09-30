from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_phase3_routes_registered():
    paths={r.path for r in app.routes}
    assert "/api/research" in paths
    assert "/api/vision/analyze" in paths
    assert "/api/files" in paths
    assert "/api/automations" in paths
