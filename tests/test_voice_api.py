from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_voice_routes_exist():
 paths={r.path for r in app.routes}
 assert "/api/voice/transcribe" in paths
 assert "/api/voice/speak" in paths
