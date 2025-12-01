from typing import Dict, Any
import httpx

OFF_URL = "https://world.openfoodfacts.org/api/v2/product/{barcode}.json"


def _parse_quantity(q: str) -> Dict[str, Any]:
    # προσπαθεί να βγάλει ποσότητα (αριθμό) και μονάδα από string π.χ. "500 g", "1 kg", "250ml"
    if not q:
        return {"qty": 0.0, "unit": "piece"}
    s = q.strip().lower().replace(",", ".")
    num = []
    for ch in s:
        if ch.isdigit() or ch == ".":
            num.append(ch)
        else:
            break
    try:
        val = float("".join(num)) if num else 0.0
    except ValueError:
        val = 0.0

    unit = "piece"
    if "kg" in s:
        unit = "g"
        val = val * 1000.0
    elif "g" in s:
        unit = "g"
    elif "l" in s and "ml" not in s:
        unit = "ml"
        val = val * 1000.0
    elif "ml" in s:
        unit = "ml"

    return {"qty": float(val), "unit": unit}


def _as_float(x: Any) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def fetch_product(barcode: str) -> Dict[str, Any]:
    # απλό GET στο OFF και χαρτογράφηση βασικών πεδίων
    r = httpx.get(OFF_URL.format(barcode=barcode), timeout=10)
    if r.status_code != 200:
        raise RuntimeError("product not found")

    data = r.json()
    product = data.get("product")
    if not product:
        raise RuntimeError("product not found")

    name = product.get("product_name") or ""

    qinfo = _parse_quantity(product.get("quantity", "") or "")
    qty = qinfo["qty"]
    unit = qinfo["unit"]

    nutr = product.get("nutriments") or {}
    kcal = _as_float(nutr.get("energy-kcal_100g"))
    protein = _as_float(nutr.get("protein_100g"))
    fat = _as_float(nutr.get("fat_100g"))
    carbs = _as_float(nutr.get("carbohydrates_100g"))

    return {
        "name": name,
        "qty": qty,
        "unit": unit,
        "cost": None,
        "kcal": kcal,
        "protein": protein,
        "fat": fat,
        "carbs": carbs,
    }
