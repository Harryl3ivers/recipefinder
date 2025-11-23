from main.api_client import SpoonacularClient
from main.db import get_favourites, add_favourites
from main.validate_ingredients import validate_ingredients
from unittest.mock import patch, MagicMock
import pytest
import sqlite3
import os 

class TestEndToEnd:
    @pytest.fixture(autouse=True)
    def setup_db(self ):
        self.test_db_name = "test_e2e_recipes.db"
        if os.path.exists(self.test_db_name):
            os.remove(self.test_db_name)
        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS recipes
                          (id INTEGER PRIMARY KEY,
                           title TEXT,
                           ingredients TEXT,
                           readyInMinutes INTEGER,
                           instructions TEXT,
                           time INTEGER,
                           cuisine TEXT,
                           image TEXT,
                           sourceUrl TEXT,
                           mealType TEXT)''')
        conn.commit()
        conn.close()

        yield
        if os.path.exists(self.test_db_name):
            os.remove(self.test_db_name)

    
    def _recipe_details(self,recipe_id,title,mealType="breakfast"):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": recipe_id,
            "title": title,
            "extendedIngredients": [
                {"name": "ingredient1", "amount": 100},
                {"name": "ingredient2", "amount": 50}
            ],
            "readyInMinutes": 20,
            "analyzedInstructions": [
                {
                    "steps": [
                        {"number": 1, "step": "Step 1"},
                        {"number": 2, "step": "Step 2"}
                    ]
                }
            ],

            "maxReadyTime": 25,
            "cuisines": ["Italian"],
            "image": f"http://example.com/{recipe_id}.jpg",
            "sourceUrl": f"http://example.com/recipe/{recipe_id}",
            "type": mealType

        }
        return mock_response
    
    def mock_search_response_helper(self,recipe_id):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [{"id": rid} for rid in recipe_id]
        }
        return mock_response
    @patch('main.api_client.requests.get')
    def test_search_recipe_and_save(self,mock_get):
        mock_search = self.mock_search_response_helper([131,213])
        mock_dish_1 = self._recipe_details(131,"Tomato pizza","dinner")
        mock_dish_2 = self._recipe_details(213,"Chicken soup","lunch")
        mock_get.side_effect = [mock_search, mock_dish_1, mock_dish_2]

        #validate ingredients
        user_ingredients = "tomato, cheese, chicken"
        ingredients_list = validate_ingredients(user_ingredients)
        assert len(ingredients_list) == 3
        assert "tomato" in ingredients_list
        assert "cheese" in ingredients_list
        assert "chicken" in ingredients_list
        #search recipes
        client = SpoonacularClient()
        recipes = client.search_recipes(query="", ingredients=",".join(ingredients_list), meal_type=None, number=2)
        assert len(recipes) == 2
        
        #Verify
        assert recipes[0]['title'] == "Tomato pizza"
        assert recipes[1]['title'] == "Chicken soup"
       
        #Save to favourites
        add_favourites(recipes[0],db_path=self.test_db_name)
        add_favourites(recipes[1],db_path=self.test_db_name)

        #Retrieve from favourites
        favourites = get_favourites(db_path=self.test_db_name)
        assert len(favourites) == 2



    







        

