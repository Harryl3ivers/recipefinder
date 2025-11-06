from api_client import SpoonacularClient
from validate_ingredients import validate_ingredients
from db import add_favourites, get_favourites

def main():
    print("🍳 Recipe Finder\n")
    
    ingredients = input("Enter ingredients you have (comma-separated): ")
    ingredients_list = validate_ingredients(ingredients)
    mealType = input("Enter meal type (optional, e.g. breakfast, lunch, dinner): ") or None


    
    try:
        client = SpoonacularClient()
        recipes = client.search_recipes(query="", ingredients=",".join(ingredients_list), meal_type= mealType, number=5)
        
        if not recipes:
            print("❌ No recipes found with the given ingredients.")
        else:
            print(f"\n✅ Found {len(recipes)} recipes!\n")
            
            # Display recipes nicely
            for recipe in recipes:
                print(f"📖 {recipe['title']}")
                print(f"   ⏱️  {recipe['readyInMinutes']} minutes")
                print(f"   🔗 {recipe['sourceUrl']}")
                
                # Check and display instructions
                if recipe.get("instructions") and len(recipe["instructions"]) > 0:  #does instructions exist and is it not None and does list have 1 item
                    steps = recipe["instructions"][0].get("steps", []) #get steps from first instruction block and get steps
                    if steps:
                        print(f"   📝 Instructions:")
                        for step in steps:  #loop through steps
                            print(f"      Step {step['number']}: {step['step']}")
                else:
                    print(f"   📝 No instructions available")
                
                print()  # Empty line between recipes
            for recipe in recipes:
                save = input(f"Do you want to save '{recipe['title']}' to favourites? (y/n): ").strip().lower()
                if save == 'y':
                    add_favourites(recipe)
                    print(f"✅ '{recipe['title']}' added to favourites!\n")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()