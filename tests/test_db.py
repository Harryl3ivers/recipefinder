import pytest
import sqlite3
import json
import os

from main.db import add_favourites, get_favourites
@pytest.fixture
def test_db():
    test_db_name = 'test_recipes.db'

    if os.path.exists(test_db_name):
        os.remove(test_db_name)
    
    conn = sqlite3.connect(test_db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            title TEXT,
            ingredients TEXT,
            readyInMinutes INTEGER,
            instructions TEXT,
            time INTEGER,
            cuisine TEXT,
            image TEXT,
            sourceUrl TEXT,
            mealType TEXT
        )
    ''')
    conn.commit()
    
    yield test_db_name
    
    # Teardown
    if os.path.exists(test_db_name):
        os.remove(test_db_name)

def test_add_favourites(test_db):
  
    
    sample_recipe = {
        'id': 1,
        'title': 'Test Recipe',
        'ingredients': [{'name': 'ingredient1'}, {'name': 'ingredient2'}],
        'instructions': [{'steps': ['step1', 'step2']}],
        'readyInMinutes': 30,
        'sourceUrl': 'http://example.com',
        'image': 'http://example.com/image.jpg',
        'mealType': 'dinner'
    }
    
    add_favourites(sample_recipe,test_db)
    favourites = get_favourites(test_db)
    assert len(favourites) == 1
    assert favourites[0]['title'] == 'Test Recipe'
    
   
def test_get_favourites_empty(test_db):
    favourites = get_favourites(test_db)
    assert len(favourites) == 0

def test_add_multiple_favourites(test_db):
    sample_recipe1 = {
        "id": 1,
        "title": "Test Recipe 1",
        "ingredients": [{"name": "ingredient1"}],
        "instructions": [{"steps": ["step1"]}],
        "readyInMinutes": 20,
        "sourceUrl": "http://example.com/1",
        "image": "http://example.com/image1.jpg",
        "mealType": "lunch"
    }
    sample_recipe2 = {
        "id": 2,
        "title": "Test Recipe 2",
        "ingredients": [{"name": "ingredient2"}],
        "instructions": [{"steps": ["step2"]}],
        "readyInMinutes": 40,
        "sourceUrl": "http://example.com/2",
        "image": "http://example.com/image2.jpg",
        "mealType": "dinner"
    }
    add_favourites(sample_recipe1,test_db)
    add_favourites(sample_recipe2,test_db)
    favourites = get_favourites(test_db)
    assert len(favourites) == 2
    titles = [fav['title'] for fav in favourites]
    assert "Test Recipe 1" in titles
    assert "Test Recipe 2" in titles

def test_duplicate_favourite(test_db):
    sample_recipe = {
        "id": 1,
        "title": "Test Recipe",
        "ingredients": [{"name": "ingredient1"}],
        "instructions": [{"steps": ["step1"]}],
        "readyInMinutes": 20,
        "sourceUrl": "http://example.com",
        "image": "http://example.com/image.jpg",
        "mealType": "lunch"
    }
    add_favourites(sample_recipe,test_db)
    add_favourites(sample_recipe,test_db)  # Add the same recipe again
    favourites = get_favourites(test_db)
    assert len(favourites) == 1  # Should still be only one entry

def test_favourite_data_integrity(test_db):
    sample_recipe = {
        "id": 1,
        "title": "Integrity Test Recipe",
        "ingredients": [{"name": "ingredient1"}, {"name": "ingredient2"}],
        "instructions": [{"steps": ["step1", "step2"]}],
        "readyInMinutes": 25,
        "sourceUrl": "http://example.com/integrity",
        "image": "http://example.com/image_integrity.jpg",
        "mealType": "breakfast"
    }
    add_favourites(sample_recipe,test_db)
    favourites = get_favourites(test_db)
    assert len(favourites) == 1
    fav = favourites[0]
    assert fav['id'] == sample_recipe['id']
    assert fav['title'] == sample_recipe['title']
    assert fav['ingredients'] == sample_recipe['ingredients']
    assert fav['instructions'] == sample_recipe['instructions']
    assert fav['readyInMinutes'] == sample_recipe['readyInMinutes']
    assert fav['sourceUrl'] == sample_recipe['sourceUrl']
    assert fav['image'] == sample_recipe['image']
    assert fav['mealType'] == sample_recipe['mealType']

    

    
 