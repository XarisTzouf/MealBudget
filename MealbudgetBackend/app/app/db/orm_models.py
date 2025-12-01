from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base

# Many-to-many συσχετισμός Plan <-> Meal
plan_meal = Table(
    "plan_meal",
    Base.metadata,
    Column("plan_id", ForeignKey("plans.id"), primary_key=True),
    Column("meal_id", ForeignKey("meals.id"), primary_key=True),
)

class Meal(Base):
    __tablename__ = "meals"  # πίνακας προϊόντων/γευμάτων

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, default="main")
    cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    kcal: Mapped[float | None] = mapped_column(Float, nullable=True)
    protein: Mapped[float | None] = mapped_column(Float, nullable=True)
    fat: Mapped[float | None] = mapped_column(Float, nullable=True)
    carbs: Mapped[float | None] = mapped_column(Float, nullable=True)

class Plan(Base):
    __tablename__ = "plans"  # πίνακας πλάνων

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    budget: Mapped[float] = mapped_column(Float, nullable=False)

    # λίστα γευμάτων που ανήκουν στο πλάνο
    meals = relationship("Meal", secondary=plan_meal, lazy="selectin", backref="plans")
