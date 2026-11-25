import os

os.environ["MEMORY_TOKEN"] = "test-memory-token"
from fastapi.testclient import TestClient
from memory.main import app


def test_memory_requires_auth_and_dependencies():
    with TestClient(app) as c:
        assert c.get("/healthz").status_code == 401
        h = {"Authorization": "Bearer test-memory-token"}
        assert c.get("/healthz", headers=h).json()["status"] == "blocked"
        payload = {
            "group_id": "vitruvius:project:p1",
            "name": "decision",
            "text": "approved fact",
            "approved": False,
        }
        assert c.post("/episodes", headers=h, json=payload).status_code == 422
        payload["approved"] = True
        assert c.post("/episodes", headers=h, json=payload).status_code == 503
        payload["group_id"] = "other-tenant:all"
        assert c.post("/episodes", headers=h, json=payload).status_code == 422


def test_graphiti_openrouter_constructor(monkeypatch):
    from memory.main import build_graphiti

    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("NEO4J_PASSWORD", "test-password")
    graph = build_graphiti()
    assert str(graph.llm_client.client.base_url) == "https://openrouter.ai/api/v1/"
    assert graph.llm_client.structured_output_mode == "json_object"
    assert str(graph.embedder.client.base_url) == "https://openrouter.ai/api/v1/"
