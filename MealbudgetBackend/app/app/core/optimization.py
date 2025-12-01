import random
from app.core.domain_models import PlanRequest, PlanResponse, PlanRow

def solve(req: PlanRequest) -> PlanResponse:
    # 1. Φιλτράρισμα και Ομαδοποίηση ανά Κατηγορία
    breakfast_items = [c for c in req.candidates if c.category == 'breakfast' and c.cost <= req.budget]
    main_items = [c for c in req.candidates if c.category == 'main' and c.cost <= req.budget]
    snack_items = [c for c in req.candidates if c.category == 'snack' and c.cost <= req.budget]
    
    # Ανακάτεμα για ποικιλία
    random.shuffle(breakfast_items)
    random.shuffle(main_items)
    random.shuffle(snack_items)

    quantities = {} # {meal_id: qty}
    current_cost = 0.0
    current_kcal = 0.0
    
    # Στόχος: Εβδομαδιαίες θερμίδες (αν δεν δόθηκε, υποθέτουμε 14000 = 2000*7)
    target_kcal = req.kcal_target if req.kcal_target else 14000.0

    # ---------------------------------------------------------
    # ΛΟΓΙΚΗ ΕΒΔΟΜΑΔΑΣ (7 ΗΜΕΡΕΣ)
    # ---------------------------------------------------------
    for day in range(7):
        # Αν τελείωσαν τα λεφτά, σταματάμε
        if current_cost >= req.budget:
            break

        # --- Α. ΕΠΙΛΟΓΗ ΠΡΩΙΝΟΥ ---
        if breakfast_items:
            # Διαλέγουμε ένα τυχαίο πρωινό
            bf = random.choice(breakfast_items)
            if current_cost + bf.cost <= req.budget:
                quantities[bf.meal_id] = quantities.get(bf.meal_id, 0) + 1
                current_cost += bf.cost
                current_kcal += bf.kcal

        # --- Β. ΕΠΙΛΟΓΗ ΜΕΣΗΜΕΡΙΑΝΟΥ (Κυρίως) ---
        if main_items:
            lunch = random.choice(main_items)
            if current_cost + lunch.cost <= req.budget:
                quantities[lunch.meal_id] = quantities.get(lunch.meal_id, 0) + 1
                current_cost += lunch.cost
                current_kcal += lunch.kcal

        # --- Γ. ΕΠΙΛΟΓΗ ΒΡΑΔΙΝΟΥ (Κυρίως) ---
        if main_items:
            dinner = random.choice(main_items) # Μπορεί να είναι ίδιο ή άλλο
            if current_cost + dinner.cost <= req.budget:
                quantities[dinner.meal_id] = quantities.get(dinner.meal_id, 0) + 1
                current_cost += dinner.cost
                current_kcal += dinner.kcal

    # --- Δ. ΣΥΜΠΛΗΡΩΜΑ ΜΕ SNACKS (Αν περισσεύουν λεφτά/θερμίδες) ---
    while current_cost < req.budget and current_kcal < target_kcal and snack_items:
        snack = random.choice(snack_items)
        if current_cost + snack.cost <= req.budget:
             quantities[snack.meal_id] = quantities.get(snack.meal_id, 0) + 1
             current_cost += snack.cost
             current_kcal += snack.kcal
        else:
             # Αν δεν χωράει το συγκεκριμένο σνακ, δοκίμασε άλλο (ή σταμάτα αν είναι ακριβά όλα)
             break

    # ---------------------------------------------------------
    # ΔΗΜΙΟΥΡΓΙΑ ΑΠΟΤΕΛΕΣΜΑΤΟΣ
    # ---------------------------------------------------------
    rows = []
    candidates_map = {c.meal_id: c for c in req.candidates}

    total_cost = 0.0
    total_kcal = 0.0
    total_protein = 0.0
    total_fat = 0.0
    total_carbs = 0.0

    for m_id, qty in quantities.items():
        original = candidates_map[m_id]
        
        rows.append(PlanRow(
            meal_id=original.meal_id,
            name=original.name,
            qty=qty,
            cost=original.cost,
            kcal=original.kcal,
            protein=original.protein,
            fat=original.fat,
            carbs=original.carbs
        ))
        
        total_cost += original.cost * qty
        total_kcal += original.kcal * qty
        total_protein += original.protein * qty
        total_fat += original.fat * qty
        total_carbs += original.carbs * qty

    # Sort για να φαίνονται όμορφα (π.χ. αλφαβητικά)
    rows.sort(key=lambda x: x.name)

    return PlanResponse(
        title=req.title,
        rows=rows,
        total_cost=total_cost,
        total_kcal=total_kcal,
        total_protein=total_protein,
        total_fat=total_fat,
        total_carbs=total_carbs,
    )