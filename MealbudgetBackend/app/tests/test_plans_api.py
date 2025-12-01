# tests/test_plans_api.py
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import Base, engine, SessionLocal
from app.db import orm_models as models

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Καθαρίζει και ξαναφτιάχνει τη βάση πριν από κάθε test και κάνει seed 2 meals."""
    # Drop & create όλα τα tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Seed δεδομένα
    db = SessionLocal()
    try:
        m1 = models.Meal(
            name="Chicken Salad",
            cost=5.0,
            kcal=400.0,
            protein=30.0,
            fat=10.0,
            carbs=20.0,
        )
        m2 = models.Meal(
            name="Pasta Bolognese",
            cost=7.0,
            kcal=800.0,
            protein=25.0,
            fat=20.0,
            carbs=90.0,
        )
        db.add_all([m1, m2])
        db.commit()
        yield
    finally:
        db.close()


def test_create_and_get_plan():
    # Χρησιμοποιούμε τα ids 1 και 2 από τα seeded meals
    payload = {
        "title": "Week A",
        "budget": 20.0,
        "meal_ids": [1, 2],
    }
    r = client.post("/plans", json=payload)
    assert r.status_code == 201
    body = r.json()

    assert body["title"] == "Week A"
    assert body["budget"] == 20.0
    assert "id" in body
    assert len(body["meals"]) == 2
    names = {m["name"] for m in body["meals"]}
    assert names == {"Chicken Salad", "Pasta Bolognese"}

    plan_id = body["id"]

    # GET /plans/{id}
    r2 = client.get(f"/plans/{plan_id}")
    assert r2.status_code == 200
    body2 = r2.json()
    assert body2["id"] == plan_id
    assert body2["title"] == "Week A"
    assert len(body2["meals"]) == 2


def test_get_plan_stats():
    # Δημιούργησε plan πρώτα
    payload = {
        "title": "Stats Plan",
        "budget": 50.0,
        "meal_ids": [1, 2],
    }
    r = client.post("/plans", json=payload)
    assert r.status_code == 201
    plan_id = r.json()["id"]

    # GET /plans/{id}/stats
    r2 = client.get(f"/plans/{plan_id}/stats")
    assert r2.status_code == 200
    stats = r2.json()

    # Ελέγχουμε τα αθροίσματα: cost/kcal/protein/fat/carbs
    # Chicken Salad:   cost=5, kcal=400, protein=30, fat=10, carbs=20
    # Pasta Bolognese: cost=7, kcal=800, protein=25, fat=20, carbs=90
    # Σύνολα: cost=12, kcal=1200, protein=55, fat=30, carbs=110
    assert stats["plan_id"] == plan_id
    assert stats["total_cost"] == 12.0
    assert stats["kcal"] == 1200.0
    assert stats["protein"] == 55.0
    assert stats["fat"] == 30.0
    assert stats["carbs"] == 110.0


def test_create_plan_with_unknown_meal():
    # meal_ids περιέχει id που δεν υπάρχει (π.χ. 999)
    payload = {
        "title": "Invalid Plan",
        "budget": 10.0,
        "meal_ids": [999],
    }
    r = client.post("/plans", json=payload)
    assert r.status_code == 404
    body = r.json()
    assert body["detail"] == "Meal not found"
