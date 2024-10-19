# HACKATHON FALL SEMESTER 2024 #
# DYLAN KOHN, JONATHAN NELSON, JONATHAN ASCONA #
# 10/18/24 - 10/19/24)


import requests
import json
import os
import re
import csv
import pytesseract
from PIL import Image

# Your Spoonacular API key
API_KEY = "1e489973c24e437b92a3571cb5ef0e18"

# File to store saved recipes
SAVED_RECIPES_FILE = "saved_recipes.json"
INGREDIENTS_FILE = "ingredients.txt"

# Function to save ingredients to a list and store them in a text file
def add_ingredients_to_list(ingredients, filename=INGREDIENTS_FILE):
    with open(filename, 'a') as file:
        file.write(", ".join(ingredients) + "\n")
    print(f"Ingredients '{', '.join(ingredients)}' have been added to the list.")

# Function to load previously entered ingredients from a text file
def load_ingredients_from_file(filename=INGREDIENTS_FILE):
    try:
        with open(filename, 'r') as file:
            content = file.readlines()
            ingredients = [line.strip() for line in content]
            return ingredients
    except FileNotFoundError:
        return []

# Function to clear the ingredients text file
def clear_ingredients_file(filename=INGREDIENTS_FILE):
    with open(filename, 'w') as file:
        file.write('')  # Overwrite the file with nothing (clear the contents)
    print(f"All ingredients have been cleared from {filename}.")

# Function to parse ingredient string and detect quantity
def parse_ingredient(ingredient):
    match = re.match(r"(\d+)?\s*(.*)", ingredient)
    quantity = match.group(1) if match.group(1) else ""
    name = match.group(2).strip() if match.group(2) else ingredient
    return quantity, name

# Function to fetch recipes based on ingredients (ignoring quantities)
# Function to fetch recipes based on ingredients (and filter by missing ingredients if desired)
def get_recipe(ingredients, show_missing_ingredients):
    cleaned_ingredients = [parse_ingredient(ingredient)[1] for ingredient in ingredients]
    
    # Fetch recipes based on the ingredients provided
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={', '.join(cleaned_ingredients)}&number=5&apiKey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        recipes = response.json()
        
        if not show_missing_ingredients:
            # Filter to only include recipes that use the ingredients the user has
            recipes = [recipe for recipe in recipes if not recipe['missedIngredients']]
        
        # Add the recipe link to each recipe in the results
        for recipe in recipes:
            recipe['link'] = f"https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-').lower()}-{recipe['id']}"
        
        return recipes  # Return the filtered recipes with links
    else:
        print(f"Failed to fetch recipes. Status code: {response.status_code}")
        return None


# Function to fetch ingredient price based on ingredient ID
def get_ingredient_price(ingredient_id):
    url = f"https://api.spoonacular.com/food/ingredients/{ingredient_id}/information?apiKey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        ingredient_info = response.json()
        price = ingredient_info.get('estimatedCost', {}).get('value', None)
        if price is not None:
            return float(price)
        else:
            return None
    else:
        print(f"Failed to fetch ingredient price. Status code: {response.status_code}")
        return None

# Function to fetch recipe details, including instructions and nutrition
def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=true&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        recipe_info = response.json()
        recipe_info['link'] = f"https://spoonacular.com/recipes/{recipe_id}"  # Add the link to the recipe
        return recipe_info
    else:
        print(f"Failed to fetch recipe details. Status code: {response.status_code}")
        return None


# Function to display nutrition facts
def display_nutrition(nutrition):
    if nutrition:
        nutrients = nutrition['nutrients']
        print("Nutrition Facts:")
        for nutrient in nutrients:
            print(f"{nutrient['name']}: {nutrient['amount']} {nutrient['unit']}")
    else:
        print("No nutrition information available.")

# Function to display saved recipes
def display_saved_recipes():
    if os.path.exists(SAVED_RECIPES_FILE):
        with open(SAVED_RECIPES_FILE, 'r') as file:
            saved_recipes = json.load(file)
            if saved_recipes:
                print("\nPreviously saved recipes:")
                for idx, recipe in enumerate(saved_recipes, start=1):
                    print(f"{idx}. {recipe['title']} - {recipe['link']}")
            else:
                print("No recipes saved yet.")
    else:
        print("No saved recipes found.")

# Function to display the recipe information
# Function to display the recipe information
# Function to display the recipe information
def display_recipes(recipes, show_missing_ingredients, show_nutrition, show_instructions, show_prices):
    if recipes and len(recipes) > 0:  # Check if there's at least one recipe
        recipe = recipes[0]  # Get the first recipe only
        print(f"Recipe Title: {recipe['title']}")
        
        used_ingredients = [f"{ingredient['amount']} {ingredient['unit']} {ingredient['name']}" for ingredient in recipe['usedIngredients']]
        print(f"Used Ingredients: {used_ingredients}")
        
        if show_missing_ingredients:
            missing_ingredients = recipe['missedIngredients']
            if missing_ingredients:
                print(f"Missing Ingredients: {[ingredient['name'] for ingredient in missing_ingredients]}")
                
                if show_prices:
                    print("Prices for Missing Ingredients:")
                    for ingredient in missing_ingredients:
                        ingredient_price = get_ingredient_price(ingredient['id'])
                        if ingredient_price is not None:
                            print(f"Ingredient: {ingredient['name']} - Estimated Price: ${ingredient_price / 100:.2f}")
                        else:
                            print(f"Ingredient: {ingredient['name']} - Price not available")
            else:
                print("No missing ingredients for this recipe.")
        
        if show_instructions:
            instructions = get_recipe_details(recipe['id']).get('instructions', 'No instructions available.')
            print(f"Instructions: {instructions}")
        
        if show_nutrition:
            recipe_details = get_recipe_details(recipe['id'])
            if recipe_details:
                display_nutrition(recipe_details['nutrition'])

        print(f"Recipe Link: https://spoonacular.com/recipes/{recipe['id']}")
        print('-' * 40)
        
        # Ask the user if they want to save the recipe
        save_option = input(f"Do you want to save the recipe '{recipe['title']}'? (yes/no): ").strip().lower()
        if save_option == 'yes':
            recipe_to_save = {
                'title': recipe['title'],
                'link': f"https://spoonacular.com/recipes/{recipe['id']}",
                'used_ingredients': used_ingredients,
                'missing_ingredients': [ingredient['name'] for ingredient in missing_ingredients]
            }
            save_recipe(recipe_to_save)
    else:
        print("No recipes found.")

# Function to save a recipe to a JSON file
def save_recipe(recipe):
    if not os.path.exists(SAVED_RECIPES_FILE):
        with open(SAVED_RECIPES_FILE, 'w') as file:
            json.dump([], file)  # Initialize with an empty list if file doesn't exist
    
    with open(SAVED_RECIPES_FILE, 'r+') as file:
        recipes = json.load(file)
        recipes.append(recipe)
        file.seek(0)
        json.dump(recipes, file, indent=4)
    
    print(f"Recipe '{recipe['title']}' has been saved.")

# Function to export saved recipes to CSV
def export_saved_recipes_to_csv(csv_filename="saved_recipes.csv"):
    if os.path.exists(SAVED_RECIPES_FILE):
        with open(SAVED_RECIPES_FILE, 'r') as json_file:
            saved_recipes = json.load(json_file)
            if saved_recipes:
                with open(csv_filename, 'w', newline='') as csv_file:
                    fieldnames = ['Title', 'Link', 'Used Ingredients', 'Missing Ingredients']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    for recipe in saved_recipes:
                        writer.writerow({
                            'Title': recipe['title'],
                            'Link': recipe['link'],
                            'Used Ingredients': ', '.join(recipe['used_ingredients']),
                            'Missing Ingredients': ', '.join(recipe['missing_ingredients'])
                        })
                print(f"Saved recipes exported to {csv_filename}.")
            else:
                print("No recipes saved to export.")
    else:
        print("No saved recipes file found.")

def extract_text_from_image(image_path):
    try:
        # Open the image using PIL
        image = Image.open(image_path)
        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(image)
        return text.strip()  # Remove leading/trailing whitespace
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None

def analyze_image(image_path):
    try:
        # Extract text from the image
        extracted_text = extract_text_from_image(image_path)
        if extracted_text:
            # Split the text into lines and clean it up
            lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]
            return lines  # Return list of detected ingredients
        else:
            return None
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return None


# Main program logic
if __name__ == "__main__":
    # Ask if the user wants to clear the ingredients file
    clear_file = input("Would you like to clear all previously entered ingredients? (yes/no): ").strip().lower()
    
    if clear_file == 'yes':
        clear_ingredients_file()
    
    # Load previously entered ingredients from the file
    previous_ingredients = load_ingredients_from_file()
    
    # Display the previous ingredients
    if previous_ingredients:
        print("Previously entered ingredients:")
        for ingredients in previous_ingredients:
            print(ingredients)
    
    # Ask the user if they want to enter ingredients manually or use a photo
    input_method = input("How would you like to enter ingredients? (manual/photo): ").strip().lower()
    
    if input_method == "manual":
        user_ingredients = input("Enter ingredients (comma-separated): ").strip().split(", ")
    
    elif input_method == "photo":
        image_type = input("Is the image a 'receipt' or 'ingredients'? ").strip().lower()
        image_path = input("Enter the path to the image: ").strip()
        
        if image_type == "receipt":
            extracted_text = extract_text_from_image(image_path)
            if extracted_text:

                if extracted_text:
                    print(f"Extracted ingredients from receipt: {extracted_text}")
                    user_ingredients = extracted_text.split("\n")
        
        elif image_type == "ingredients":
            detected_ingredients = analyze_image(image_path)
            if detected_ingredients:
                print(f"Detected Ingredients: {detected_ingredients}")
                user_ingredients = [detected_ingredients]

    # Add new ingredients to the file
    add_ingredients_to_list(user_ingredients)

    # Ask the user if they want to see missing ingredients
    show_missing_ingredients = input("Would you like to see missing ingredients with available recipes? (yes/no): ").strip().lower() == 'yes'
    
    # Ask the user if they want to see recipe instructions
    show_instructions = input("Would you like to see recipe instructions? (yes/no): ").strip().lower() == 'yes'
    
    # Ask the user if they want to see the nutrition facts
    show_nutrition = input("Would you like to see nutrition facts for each recipe? (yes/no): ").strip().lower() == 'yes'
    
    # Ask the user if they want to see ingredient prices (for missing ingredients only)
    show_prices = input("Would you like to see estimated prices for the missing ingredients? (yes/no): ").strip().lower() == 'yes'

    # Fetch the recipes based on the provided ingredients
    recipes = get_recipe(user_ingredients)
    
    # Display the fetched recipes with or without missing ingredients, instructions, nutrition facts, and prices
    display_recipes(recipes, show_missing_ingredients, show_nutrition, show_instructions, show_prices)
    
    # Ask if the user wants to display previously saved recipes
    display_saved_option = input("Would you like to see your saved recipes? (yes/no): ").strip().lower()
    if display_saved_option == 'yes':
        display_saved_recipes()

    # Ask if the user wants to export saved recipes to a CSV file
    export_csv_option = input("Would you like to export your saved recipes to a CSV file? (yes/no): ").strip().lower()
    if export_csv_option == 'yes':
        export_saved_recipes_to_csv()