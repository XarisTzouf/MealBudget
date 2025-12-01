import sys
from pathlib import Path

# Project root = φάκελος που περιέχει τους φακέλους "app" και "tests"
ROOT = Path(__file__).resolve().parent.parent  # ...\MealbudgetBackend\app

# Βάλε ρητά το project root πρώτο στο sys.path
root_str = str(ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

print("[conftest] ROOT =", ROOT)
print("[conftest] sys.path[0:3] =", sys.path[0:3])

from app.main import app  # εδώ πλέον πρέπει να βρει app.main κανονικά

