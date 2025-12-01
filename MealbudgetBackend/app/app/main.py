from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.budget import router as budget_router
from app.api.endpoints.plans import router as plans_router
from app.db.database import engine
from app.db.orm_models import Base
from app.api import meals
Base.metadata.create_all(bind=engine)




from app.db.database import Base, engine
# Εισαγωγή των ORM μοντέλων ώστε να δηλωθούν οι πίνακες πριν το create_all
from app.db import orm_models as _models  # noqa: F401

app = FastAPI(title="MealBudget API", version="0.1.0")

# CORS για Flutter web (port 7357)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Δημιουργία πινάκων SQLite στην εκκίνηση
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"ok": True}

# Routers 
app.include_router(budget_router)
app.include_router(plans_router)
app.include_router(meals.router)