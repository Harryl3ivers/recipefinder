import re
def validate_ingredients(ingredients_input):
    if not ingredients_input:
        raise ValueError("No ingredients provided.")
    ingredients_list = [ingredients.strip() for ingredients in ingredients_input.split(",")] #remove extra spaces and split by comma
    if not ingredients_list:
        raise ValueError("Ingredients list is empty after processing.")
    for i in ingredients_list:
        if not re.match(r"^[a-zA-Z\s\-]+$", i):
            raise ValueError(f"Invalid ingredient: {i}. Only alphabetic characters and spaces are allowed.")
    return ingredients_list