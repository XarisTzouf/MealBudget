from typing import List, Optional
from pydantic import BaseModel, ConfigDict


# Υποψήφιο γεύμα που μπορεί να χρησιμοποιήσει ο solver.
class PlanItemCandidate(BaseModel):
    meal_id: int
    name: str
    category: str
    cost: float   # κόστος για 1 τεμάχιο/μερίδα
    kcal: float
    protein: float
    fat: float
    carbs: float


# Είσοδος του solver για /budget/optimize.
class PlanRequest(BaseModel):
    title: str
    budget: float
    candidates: List[PlanItemCandidate]
    kcal_target: Optional[float] = None
    protein_min: Optional[float] = None
    fat_max: Optional[float] = None
    carbs_max: Optional[float] = None


# Μια γραμμή του τελικού πλάνου (γεύμα με ποσότητα).
class PlanRow(BaseModel):
    meal_id: int
    name: str
    qty: int = 1
    cost: float
    kcal: float
    protein: float
    fat: float
    carbs: float


# Έξοδος solver με αναλυτικές γραμμές και σύνολα.
class PlanResponse(BaseModel):
    title: str
    rows: List[PlanRow]
    total_cost: float
    total_kcal: float
    total_protein: float
    total_fat: float
    total_carbs: float