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



def add_favourites(recipe,db_path='recipes.db'):
    conn = sqlite3.connect(db_path)
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

def get_favourites(db_path='recipes.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recipes') 
    # Tell SQLite to select all rows from the recipes table.
    rows = cursor.fetchall()
    # Fetch all those rows into Python as a list of tuples (raw data).
    conn.close()
    favourites = []
    for row in rows:
        favourites.append({
            'id': row[0],
            'title': row[1],
            'ingredients': json.loads(row[2]),
            'readyInMinutes': row[3],
            'instructions': json.loads(row[4]),
            'time': row[5],
            'cuisine': row[6],
            'image': row[7],
            'sourceUrl': row[8],
            'mealType': row[9]
        })
    return favourites

