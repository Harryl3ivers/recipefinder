import sqlite3
import json

def init_db():
    conn = sqlite3.connect('recipes.db')
    try:
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
    finally:
        conn.close()


def add_favourites(recipe, db_path='recipes.db'):
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO recipes
            (id, title, ingredients, instructions, time, cuisine, readyInMinutes, sourceUrl, image, mealType)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            recipe['id'],
            recipe['title'],
            json.dumps(recipe['ingredients']),
            json.dumps(recipe['instructions']),
            recipe.get('time'),
            json.dumps(recipe.get('cuisine')),
            recipe.get('readyInMinutes'),
            recipe.get('sourceUrl'),
            recipe.get('image'),
            recipe.get('mealType')
        ))
        conn.commit()
    finally:
        conn.close()


def get_favourites(db_path='recipes.db'):
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipes")
        rows = cursor.fetchall()
        favourites = []
        for row in rows:
            favourites.append({
                'id': row[0],
                'title': row[1],
                'ingredients': json.loads(row[2]) if row[2] else [],
                'readyInMinutes': row[3],
                'instructions': json.loads(row[4]) if row[4] else [],
                'time': row[5],
                'cuisine': json.loads(row[6]) if row[6] else [],
                'image': row[7],
                'sourceUrl': row[8],
                'mealType': row[9]
            })
        return favourites
    finally:
        conn.close()