from typing import Optional, Dict, Any, List, Tuple



# Επιστρέφει 0.0 αν x είναι None, αλλιώς float(x).

def safe_float(x: Optional[float]) -> float:
    return 0.0 if x is None else float(x)


# Ασφαλής διαίρεση: αν b==0 επιστρέφει 0.0, αλλιώς a / b.
def safe_div(a: float, b: float) -> float:
    return 0.0 if b == 0 else a / b


# Στρογγυλοποίηση σε 2 δεκαδικά.
def round2(x: float) -> float:
    return round(float(x), 2)


# Μετατρέπει μονάδες στη “βάση”:
# Άγνωστη μονάδα -> επέστρεψε (qty, unit) όπως είναι.
def to_base_qty(qty: float, unit: str) -> Tuple[float, str]:
    u = (unit or "").strip().lower()
    if u == "kg":
        return qty * 1000.0, "g"
    if u == "g":
        return qty, "g"
    if u == "l":
        return qty * 1000.0, "ml"
    if u == "ml":
        return qty, "ml"
    if u in ("piece", "τμχ"):
        return qty, "piece"
    return qty, unit


# Υπολογίζει τιμή ανά 100 (g/ml)
def per_100(value: float, qty_in_g_or_ml: float) -> float:
    return value * safe_div(100.0, qty_in_g_or_ml)


# Επιστρέφει kcal/protein/fat/carbs ανά 100g/ml.
# Αν μονάδα άγνωστη ή qty=0 -> επιστρέφει μηδενικά.
def normalize_nutrition_per_100(
    nutri: Dict[str, Optional[float]], qty: float, unit: str
) -> Dict[str, float]:
    base_qty, base_unit = to_base_qty(qty, unit)
    kcal = safe_float(nutri.get("kcal"))
    protein = safe_float(nutri.get("protein"))
    fat = safe_float(nutri.get("fat"))
    carbs = safe_float(nutri.get("carbs"))

    if base_unit == "piece":
        return {"kcal": kcal, "protein": protein, "fat": fat, "carbs": carbs}

    if base_unit in ("g", "ml") and base_qty > 0:
        return {
            "kcal": per_100(kcal, base_qty),
            "protein": per_100(protein, base_qty),
            "fat": per_100(fat, base_qty),
            "carbs": per_100(carbs, base_qty),
        }

    return {"kcal": 0.0, "protein": 0.0, "fat": 0.0, "carbs": 0.0}



# Υπολογίζει τιμή ανά 100g/ml. 
# Άγνωστη μονάδα ή qty=0 -> 0.0.
def price_per_100(cost: float, qty: float, unit: str) -> float:
    base_qty, base_unit = to_base_qty(qty, unit)
    c = safe_float(cost)
    if base_unit == "piece":
        return c
    if base_unit in ("g", "ml") and base_qty > 0:
        return per_100(c, base_qty)
    return 0.0


# Αθροίζει σύνολα από λίστα “γραμμών πλάνου”.
# Κάθε row αναμένεται να έχει: qty, cost, kcal, protein, fat, carbs.
# Επιστρέφει dict με: total_cost, total_kcal, total_protein, total_fat, total_carbs.

def aggregate_rows(rows: List[Dict[str, Any]]) -> Dict[str, float]:
    total_cost = 0.0
    total_kcal = 0.0
    total_protein = 0.0
    total_fat = 0.0
    total_carbs = 0.0

    for r in rows:
        q = safe_float(r.get("qty")) or 1.0
        total_cost += safe_float(r.get("cost")) * q
        total_kcal += safe_float(r.get("kcal")) * q
        total_protein += safe_float(r.get("protein")) * q
        total_fat += safe_float(r.get("fat")) * q
        total_carbs += safe_float(r.get("carbs")) * q

    return {
        "total_cost": total_cost,
        "total_kcal": total_kcal,
        "total_protein": total_protein,
        "total_fat": total_fat,
        "total_carbs": total_carbs,
    }


# Παίρνει προϊόν με πεδία:
#   name, cost, qty, unit, kcal/protein/fat/carbs (για όλη τη συσκευασία)
# Επιστρέφει επιπλέον:
#   qty_base, unit_base, kcal_100, protein_100, fat_100, carbs_100, price_100

def normalize_product_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    qty = safe_float(rec.get("qty"))
    unit = (rec.get("unit") or "").strip()
    cost = safe_float(rec.get("cost"))

    qty_base, unit_base = to_base_qty(qty, unit)
    nutri = {
        "kcal": rec.get("kcal"),
        "protein": rec.get("protein"),
        "fat": rec.get("fat"),
        "carbs": rec.get("carbs"),
    }
    per100 = normalize_nutrition_per_100(nutri, qty, unit)
    price100 = price_per_100(cost, qty, unit)

    out = dict(rec)
    out.update(
        {
            "qty_base": qty_base,
            "unit_base": unit_base,
            "kcal_100": per100["kcal"],
            "protein_100": per100["protein"],
            "fat_100": per100["fat"],
            "carbs_100": per100["carbs"],
            "price_100": price100,
        }
    )
    return out
