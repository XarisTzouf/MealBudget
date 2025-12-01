import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent  # ...\MealbudgetBackend\app


root_str = str(ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

print("[conftest] ROOT =", ROOT)
print("[conftest] sys.path[0:3] =", sys.path[0:3])

from app.main import app  

