# Vercel serverless entry: run the FastAPI app from the repo root (backend).
import sys
import os

# Add parent so "main" and getRecipesAndIngredients, findSnapStores, etc. resolve
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from main import app
