from main.api_client import SpoonacularClient 
from unittest.mock import patch, MagicMock
import pytest
import unittest
import requests
class TestSpoonacularClient:
    @patch('main.api_client.requests.get')
    def test_search_recipies(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {"id": 1, "title": "Test Recipe 1", "ingredients":[], "readyInMinutes":10, "time":15, "cuisine":[],"image":"","sourceUrl":[] ,"cuisine":"","mealType":""},
                {"id": 2, "title": "Test Recipe 2", "ingredients":[], "readyInMinutes":10, "time":15, "cuisine":[],"image":"","sourceUrl":[] ,"cuisine":"","mealType":""},
            ]
        }

        mock_get.return_value = mock_response
        client = SpoonacularClient()
        recipies = client.search_recipes(query="", ingredients="tomato,cheese", number=2)
        assert len(recipies) == 2
        
    @patch('main.api_client.requests.get')
    def test_search_recipies_without_meal_type(self, mock_get):
        mock_reresponse = MagicMock()
        mock_reresponse.json.return_value = {
            "results": [
                {"id": 1, "title": "Test Recipe 1", "ingredients":[], "readyInMinutes":10, "time":15, "cuisine":[],"image":"","sourceUrl":[] ,"cuisine":""},
                {"id": 2, "title": "Test Recipe 2", "ingredients":[], "readyInMinutes":10, "time":15, "cuisine":[],"image":"","sourceUrl":[] ,"cuisine":""},
            ]
        }
        mock_get.return_value = mock_reresponse
        client = SpoonacularClient()
        recipies = client.search_recipes(query="", ingredients="tomato,cheese", number=2)
        assert len(recipies) == 2
    
    @patch('main.api_client.requests.get')
    def test_get_recipe_details(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": 1,
            "title": "Test Recipe 1",
            "extendedIngredients": [{"name": "ingredient1"}, {"name": "ingredient2"}],
            "readyInMinutes": 10,
            "analyzedInstructions": [{"steps": ["step1", "step2"]}],
            "maxReadyTime": 15,
            "cuisines": ["Italian"],
            "mealType": "dinner",
            "image": "http://example.com/image.jpg",
            "sourceUrl": "http://example.com/recipe",
            "type": "dinner"
        }
        mock_get.return_value = mock_response
        client = SpoonacularClient()
        recipe = client.get_recipe_details(recipe_id=1)
        assert recipe['id'] == 1
        assert recipe['title'] == "Test Recipe 1"
        assert len(recipe['ingredients']) == 2
        assert recipe['readyInMinutes'] == 10
        assert len(recipe['instructions']) == 1
        assert recipe['mealType'] == "dinner"
    
    @patch('main.api_client.requests.get')
    def test_search_recipes_empty_results(self,mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": []
        }
        mock_get.return_value = mock_response
        client = SpoonacularClient()
        recipes = client.search_recipes(query="", ingredients="invalidingredient", number=2)
        assert len(recipes) == 0
    
    @patch('main.api_client.requests.get')
    def test_search_recipes_api_failure(self,mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 not found")
        mock_get.return_value = mock_response
        client = SpoonacularClient()
        with pytest.raises(requests.exceptions.HTTPError):
            client.search_recipes(query="", ingredients="tomato,cheese", number=2)
    
    @patch('main.api_client.requests.get')
    def test_api_timeout(self,mock_get):
        mock_get.side_effect = requests.exceptions.Timeout
        client = SpoonacularClient()
        with pytest.raises(requests.exceptions.Timeout):
            client.search_recipes(query="", ingredients="tomato,cheese", number=2)
    
    @patch('main.api_client.requests.get')
    def test_get_recipe_details_missing_fields(self,mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id":1,

        }
        mock_get.return_value = mock_response
        client = SpoonacularClient()
        recipe = client.get_recipe_details(recipe_id=1)
        assert recipe['id'] == 1
        assert recipe['title'] is None
        assert recipe['ingredients'] is None
        