import requests
from dotenv import load_dotenv
import os


class SpoonacularClient:
    BASE_URL = "https://api.spoonacular.com"

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables.")

    def search_recipes(self, query, ingredients, number=10):
        url = f"{self.BASE_URL}/recipes/complexSearch"
        params = {
            "q": query,
            "ingredients": ingredients,
            "apiKey": self.api_key,
            "number": number,
            "ignorePantry": True,
            "ranking": 2,
        }
        requests_response = requests.get(url, params=params)
        requests_response.raise_for_status()
        data = requests_response.json()

        recipies = []  # List to hold recipe details
        for item in data.get("results", []):
            recipie = self.get_recipe_details(item["id"])
            recipies.append(recipie)
        return recipies

    def get_recipe_details(self, recipe_id):
        url = f"{self.BASE_URL}/recipes/{recipe_id}/information"
        params = {"apiKey": self.api_key, "includeNutrition": False}
        try:
            requests_response = requests.get(url, params=params)
            data = requests_response.json()

           

            recipie = {
                "id": data.get("id"),
                "title": data.get("title"),
                "ingredients": data.get("extendedIngredients"),
                "readyInMinutes": data.get("readyInMinutes"),
                "instructions": data.get("analyzedInstructions"), #no need for steps as this has steps inside it
                "time": data.get("maxReadyTime"),
                "cuisine": data.get("cuisines"),
                "image": data.get("image"),
                "sourceUrl": data.get("sourceUrl"),
            }
            
                 
            return recipie
        except requests.RequestException as e:
            print(f"Error fetching recipe details: {e}")
            return None
