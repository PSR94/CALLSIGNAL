from __future__ import annotations

from fastapi.testclient import TestClient

from callsignal.app import app


client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_demo_scenarios_available():
    response = client.get("/demo/scenarios")
    assert response.status_code == 200
    assert response.json()
