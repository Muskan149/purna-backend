"""
FastAPI backend for Poorna-Pool.
Recipes, SNAP stores, location, and distance endpoints.
"""
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Poorna-Pool API",
    description="Recipes, SNAP store finder, and location utilities",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request/Response models ---

class RecipeRequest(BaseModel):
    user_context: str = Field(..., description="User context for recipe suggestions (budget, diet, family size, etc.)")


# --- Health ---

@app.get("/")
def root():
    return {"message": "Poorna-Pool API", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "ok"}


# --- Recipes & ingredients ---

@app.post("/recipes")
def get_recipes(request: RecipeRequest):
    """Get recipes and grocery list from OpenAI based on user context."""
    try:
        from getRecipesAndIngredients import (
            get_recipes_and_ingredients,
            process_recipes,
            process_ingredients,
            process_reasoning,
        )
        raw = get_recipes_and_ingredients(request.user_context)
        recipes = process_recipes(raw)
        ingredients = process_ingredients(raw)
        reasoning = process_reasoning(raw)
        return {
            "recipes": recipes,
            "groceryList": ingredients,
            "reasoning": reasoning,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- SNAP stores ---

@app.get("/snap-stores/closest")
def closest_snap_stores(
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude"),
    zip_code: Optional[str] = Query(None, description="ZIP code"),
    k: int = Query(10, ge=1, le=50, description="Number of stores"),
):
    """Get closest SNAP retailers by coordinates or ZIP code."""
    if zip_code:
        from findSnapStores import get_closest_snap_stores_by_zip
        return get_closest_snap_stores_by_zip(zip_code, k=k)
    if lat is not None and lon is not None:
        from findSnapStores import get_closest_snap_stores
        return get_closest_snap_stores(lat, lon, k=k)
    raise HTTPException(
        status_code=400,
        detail="Provide either (lat, lon) or zip_code",
    )


# --- Location + SNAP stores ---

@app.get("/location-stores")
def location_and_stores(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    k: int = Query(10, ge=1, le=50),
):
    """Validate coordinates and return location plus closest SNAP stores."""
    try:
        from getUserLocation import get_location_and_closest_snap_stores
        return get_location_and_closest_snap_stores(lat, lon, k=k)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Distance ---

@app.get("/distance")
def distance(
    lat1: float = Query(..., description="Latitude of first point"),
    lon1: float = Query(..., description="Longitude of first point"),
    lat2: float = Query(..., description="Latitude of second point"),
    lon2: float = Query(..., description="Longitude of second point"),
):
    """Distance in miles between two points (approximate)."""
    from distanceBetween import distance_between_two_points
    miles = distance_between_two_points(lat1, lon1, lat2, lon2)
    return {"distance_miles": miles}
