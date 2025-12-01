from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# Schema για ανάγνωση Meal από τη βάση (output προς frontend).
# Χρησιμοποιεί from_attributes=True για να μπορεί να "διαβάσει" από ORM αντικείμενα.
class MealRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int                   # μοναδικό αναγνωριστικό στη ΒΔ
    name: str                 # όνομα γεύματος/προϊόντος
    category: str             # κατηγορία γεύματος (π.χ. breakfast, main, snack)
    cost: Optional[float] = None    # κόστος (π.χ. € ανά μερίδα), μπορεί να λείπει
    kcal: Optional[float] = None    # θερμίδες
    protein: Optional[float] = None # πρωτεΐνη (g)
    fat: Optional[float] = None     # λιπαρά (g)
    carbs: Optional[float] = None   # υδατάνθρακες (g)

# Schema για δημιουργία Plan (input από frontend στο POST /plans).
# Δεν χρειάζεται from_attributes γιατί ΔΕΝ είναι ORM αντικείμενο.
class PlanCreate(BaseModel):
    title: str            # τίτλος πλάνου (π.χ. "Week A")
    budget: float         # διαθέσιμο budget για το πλάνο
    meal_ids: List[int]   # λίστα από IDs γευμάτων που θα μπουν στο πλάνο

# Schema για ανάγνωση Plan (output προς frontend).
# Περιλαμβάνει και τα MealRead ώστε το UI να έχει έτοιμα τα δεδομένα των meals.
class PlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    budget: float
    meals: List[MealRead] = []  # προεπιλογή κενή λίστα αν δεν υπάρχουν meals

# Απλό schema για στατιστικά ενός Plan (π.χ. για KPIs/γραφικά).
# Δεν βασίζεται σε ORM instance, οπότε δεν χρειάζεται from_attributes.
class PlanStats(BaseModel):
    plan_id: int      # σε ποιο plan αναφέρονται τα στατιστικά
    total_cost: float # συνολικό κόστος όλων των meals στο plan
    kcal: float       # άθροισμα θερμίδων
    protein: float    # άθροισμα πρωτεΐνης (g)
    fat: float        # άθροισμα λιπαρών (g)
    carbs: float      # άθροισμα υδατανθράκων (g)
