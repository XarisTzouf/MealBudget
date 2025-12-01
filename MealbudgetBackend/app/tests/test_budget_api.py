
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_optimize_success(monkeypatch):
    
    from app.api.endpoints import budget as budget_ep

    def fake_solve(req):
        class FakeResp(dict):
            
            pass
        return {
            "title": "ok",
            "rows": [],
            "total_cost": 0.0,
            "total_kcal": 0.0,
            "total_protein": 0.0,
            "total_fat": 0.0,
            "total_carbs": 0.0,
        }

    monkeypatch.setattr(budget_ep, "solve", fake_solve)

    payload = {
        "title": "demo",
        "budget": 10.0,
        "candidates": []
    }
    r = client.post("/budget/optimize", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "ok"
    assert body["total_cost"] == 0.0

def test_optimize_failure(monkeypatch):
    from app.api.endpoints import budget as budget_ep

    def raise_err(req):
        raise ValueError("over budget")

    monkeypatch.setattr(budget_ep, "solve", raise_err)

    payload = {
        "title": "demo",
        "budget": 1.0,
        "candidates": [{"meal_id": 1, "name": "A", "cost": 5.0, "kcal": 100, "protein": 5, "fat": 2, "carbs": 10}]
    }
    r = client.post("/budget/optimize", json=payload)
    assert r.status_code == 400
    assert r.json()["detail"] == "optimization failed"
