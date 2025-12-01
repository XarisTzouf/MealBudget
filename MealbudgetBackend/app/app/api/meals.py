from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.orm_models import Meal
from app.db.schemas import MealRead

router = APIRouter(prefix="/meals", tags=["meals"])

# Αυτό το endpoint δίνει στο Frontend τη λίστα με τα προϊόντα της βάσης
@router.get("", response_model=List[MealRead])
def get_meals(db: Session = Depends(get_db)):
    return db.query(Meal).all()