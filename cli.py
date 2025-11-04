from api_client import SpoonacularClient

def main():
    print("🍳 Recipe Finder\n")
    
    ingredients = input("Enter ingredients you have (comma-separated): ")
    ingredients_list = [ingredient.strip() for ingredient in ingredients.split(",")]
    
    try:
        client = SpoonacularClient()
        recipes = client.search_recipes(query="", ingredients=",".join(ingredients_list), number=5)
        
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
                if recipe.get("instructions") and len(recipe["instructions"]) > 0:
                    steps = recipe["instructions"][0].get("steps", [])
                    if steps:
                        print(f"   📝 Instructions:")
                        for step in steps:
                            print(f"      Step {step['number']}: {step['step']}")
                else:
                    print(f"   📝 No instructions available")
                
                print()  # Empty line between recipes
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()