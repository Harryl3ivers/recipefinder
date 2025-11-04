import sqlite3
import json
def init_db():
    conn = sqlite3.connect('recipes.db')
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
    conn.close()



def add_favourites(recipe):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO recipes
        (id, title, ingredients, instructions, readyInMinutes, sourceUrl, image, mealType)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        recipe['id'],
        recipe['title'],
        json.dumps(recipe['ingredients']),
        json.dumps(recipe['instructions']),
        recipe.get('readyInMinutes'),
        recipe.get('sourceUrl'),
        recipe.get('image'),
        recipe.get('mealType')
    ))
    conn.commit()
    conn.close()

                        