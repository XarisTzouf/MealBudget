import sys
import os

sys.path.append(os.getcwd())

from app.db.database import SessionLocal, engine
from app.db.orm_models import Base, Meal

def seed_data():
    print("  Recreating database schema...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    print("🌱 Seeding categorized meals...")

    meals = [
        # --- ΠΡΩΙΝΑ (Breakfast) ---
        Meal(name="Oats (500g)", category="breakfast", cost=1.20, kcal=1945, protein=84, fat=34, carbs=331),
        Meal(name="Greek Yogurt (1kg)", category="breakfast", cost=3.80, kcal=590, protein=100, fat=4, carbs=36),
        Meal(name="Milk 1.5% (1L)", category="breakfast", cost=1.40, kcal=470, protein=34, fat=15, carbs=50),
        Meal(name="Eggs (10 pack)", category="breakfast", cost=3.50, kcal=700, protein=60, fat=50, carbs=6),
        Meal(name="Bread Whole Wheat", category="breakfast", cost=1.80, kcal=1200, protein=40, fat=15, carbs=200),
        Meal(name="Honey (450g)", category="breakfast", cost=4.50, kcal=1300, protein=1, fat=0, carbs=350),

        # --- ΚΥΡΙΩΣ ΓΕΥΜΑΤΑ (Lunch / Dinner) ---
        Meal(name="Chicken Breast (1kg)", category="main", cost=8.50, kcal=1650, protein=310, fat=36, carbs=0),
        Meal(name="Rice (1kg)", category="main", cost=1.90, kcal=3600, protein=70, fat=6, carbs=790),
        Meal(name="Pasta (500g)", category="main", cost=0.90, kcal=1750, protein=60, fat=7, carbs=375),
        Meal(name="Tuna Can (2x160g)", category="main", cost=5.20, kcal=380, protein=84, fat=2, carbs=0),
        Meal(name="Ground Beef (500g)", category="main", cost=5.50, kcal=1250, protein=90, fat=100, carbs=0),
        Meal(name="Potatoes (1kg)", category="main", cost=1.20, kcal=770, protein=20, fat=1, carbs=170),
        Meal(name="Lentils (500g)", category="main", cost=1.60, kcal=1750, protein=120, fat=5, carbs=300),
        Meal(name="Olive Oil (1L)", category="main", cost=12.50, kcal=8840, protein=0, fat=1000, carbs=0),
        
        # --- ΣΝΑΚ (Snack) ---
        Meal(name="Banana (1kg)", category="snack", cost=1.60, kcal=890, protein=11, fat=3, carbs=228),
        Meal(name="Apples (1kg)", category="snack", cost=1.50, kcal=520, protein=3, fat=2, carbs=140),
        Meal(name="Almonds (200g)", category="snack", cost=3.50, kcal=1150, protein=42, fat=100, carbs=40),
    ]

    for m in meals:
        db.add(m)
        print(f"✅ Added [{m.category}]: {m.name}")
    
    db.commit()
    db.close()
    print("✨ Database updated successfully!")

if __name__ == "__main__":
    seed_data()