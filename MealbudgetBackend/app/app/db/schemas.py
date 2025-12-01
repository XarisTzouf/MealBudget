from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# Schema για ανάγνωση Meal από τη βάση (output προς frontend).
# Χρησιμοποιεί from_attributes=True για να μπορεί να "διαβάσει" από ORM αντικείμενα.
class MealRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int                   
    name: str                 
    category: str             
    cost: Optional[float] = None    
    kcal: Optional[float] = None    
    protein: Optional[float] = None 
    fat: Optional[float] = None     
    carbs: Optional[float] = None   

# Schema για δημιουργία Plan (input από frontend στο POST /plans).
class PlanCreate(BaseModel):
    title: str            
    budget: float         
    meal_ids: List[int]   

# Schema για ανάγνωση Plan (output προς frontend).
# Περιλαμβάνει και τα MealRead ώστε το UI να έχει έτοιμα τα δεδομένα των meals.
class PlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    budget: float
    meals: List[MealRead] = [] 

# Απλό schema για στατιστικά ενός Plan 
# Δεν βασίζεται σε ORM instance, οπότε δεν χρειάζεται from_attributes.
class PlanStats(BaseModel):
    plan_id: int      
    total_cost: float 
    kcal: float       
    protein: float    
    fat: float        
    carbs: float      
