from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Path to snap_db.csv next to this module (works when run from backend/ or from api/)
_SNAP_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snap_db.csv")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_recipes_and_ingredients(user_context):
    max_retries = 3
    last_error = None

    for attempt in range(max_retries):
        try:
            response = client.responses.create(
                prompt={
                    "id": "pmpt_699a9ed768b481958da1c8d9ac1a24db069e3574897649d4",
                    "variables": {
                        "usercontext": user_context
                    }
                },
                input=[],
                text={
                    "format": {
                        "type": "text"
                    }
                },
                reasoning={},
                max_output_tokens=2048,
                store=True,
                include=["web_search_call.action.sources"]
            )

            response_text = response.output_text

            # The response should ideally be a JSON object
            # if it is not, find the first { and return the string after it and before the last }
            if "{" in response_text:
                response_text = response_text[response_text.index("{"):response_text.rindex("}")+1]
            else:
                return json.loads("{}")  # json with empty values

            # print(type(response))
            # print(response_text)

            return json.loads(response_text)
        except json.JSONDecodeError as e:
            last_error = e
            if attempt < max_retries - 1:
                continue
            raise last_error
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                continue
            raise last_error

    raise last_error

def process_recipes(recipes_and_ingredients):
    recipes_df = pd.read_csv(_SNAP_DB_PATH)
    recipes = recipes_and_ingredients.get("recipes", [])
    for recipe in recipes:
        id = recipe.get("id", "")
        id = int(id)
        recipe["url"] = recipes_df.loc[recipes_df["id"] == id, "recipe_url"].values[0]
        recipe["name"] = recipes_df.loc[recipes_df["id"] == id, "recipe_name"].values[0]
        recipe["directions"] = recipes_df.loc[recipes_df["id"] == id, "directions"].values[0].split(" | ")
        recipe["servings"] = recipe.get("servings", 4)
        recipe["totalPrice"] = recipe.get("totalPrice", 0)
        recipe["preparationTime"] = recipe.get("preparationTime", 0)
    return recipes

def process_ingredients(recipes_and_ingredients):
    ingredients = recipes_and_ingredients.get("groceryList", [])
    for ingredient in ingredients:
        ingredient["ingredient"] = ingredient.get("ingredient", "")
        ingredient["quantity"] = ingredient.get("quantity", "")
        ingredient["pricePerUnit"] = ingredient.get("pricePerUnit", 0)
        ingredient["totalPrice"] = ingredient.get("totalPrice", 0)
    
    return ingredients

def process_reasoning(recipes_and_ingredients):
    reasoning = recipes_and_ingredients.get("reasoning", "")
    return reasoning

if __name__ == "__main__":
    user_context = "I have a family of 4 people, and we have a weekly budget of $110. My only dietary thing is that I am trying to cut down on gluten, and I'm trying to eat more heart-healthy to take care of my hypertension. "
    recipes_and_ingredients = get_recipes_and_ingredients(user_context)
    recipes = process_recipes(recipes_and_ingredients)
    ingredients = process_ingredients(recipes_and_ingredients)
    reasoning = process_reasoning(recipes_and_ingredients)
    print(recipes)
    print(ingredients)
    print(reasoning)