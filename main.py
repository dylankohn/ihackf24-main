import streamlit as st
import pandas as pd
from alternative import get_recipe, get_recipe_details
from PIL import Image
import pytesseract
import re

# Set the path for tesseract if needed
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'  # Change this to your tesseract path

# Set the page configuration
st.set_page_config(page_title="Recipe Finder", layout="wide")

# Initialize session state
if 'ingredients' not in st.session_state:
    st.session_state['ingredients'] = []  # Store ingredients as tuples (name, amount)
if 'ingredients' not in st.session_state:
    st.session_state['ingredients'] = []  # Store ingredients as tuples (name, amount)
if 'ingredient_input' not in st.session_state:
    st.session_state['ingredient_input'] = ""
if 'amount_input' not in st.session_state:
    st.session_state['amount_input'] = ""
if 'saved_recipes' not in st.session_state:
    st.session_state['saved_recipes'] = []  # Store recipe details
if 'current_recipes' not in st.session_state:
    st.session_state['current_recipes'] = []
if 'current_recipe' not in st.session_state:
    st.session_state['current_recipe'] = None

def extract_ingredients_from_image(image):
    text = pytesseract.image_to_string(image)
    ingredients = []

    # Simple regex to find potential ingredients (customize as needed)
    for line in text.split('\n'):
        # Example regex to capture typical ingredient formats
        match = re.match(r'(\d+\s?\w*)?\s*(.*)', line)
        if match:
            amount, ingredient = match.groups()
            if ingredient:  # Only add if ingredient is not empty
                ingredients.append((ingredient.strip(), amount.strip() if amount else "No amount specified"))

    return ingredients

# Function to convert the saved recipes into a CSV format
def convert_to_csv(data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

# Layout
col1, col2 = st.columns([2, 1])

# Sidebar for current ingredients and saved recipes
with col2:
    with st.sidebar:
        st.header("Saved Recipes")

        # Dropdown for saved recipes
        selected_recipe = st.selectbox("Select a recipe:", ["None"] + [recipe['title'] for recipe in st.session_state['saved_recipes']])
        
        # Display selected recipe details if not "None"
        if selected_recipe != "None":
            recipe_data = next((recipe for recipe in st.session_state['saved_recipes'] if recipe['title'] == selected_recipe), None)
            if recipe_data:
                st.subheader("Recipe Details:")
                st.markdown(f"**Title:** {recipe_data['title']}")
                if st.session_state.get('show_instructions', True):  # Check if instructions should be shown
                    st.markdown(f"**Instructions:** {recipe_data['instructions'].replace('<ol>', '').replace('</ol>', '').replace('<li>', '').replace('</li>', '').replace('<br>', '')}")  # Clean up HTML tags
                st.markdown(f"**Used Ingredients:** {', '.join(recipe_data['used_ingredients'])}")
                st.markdown(f"**Missing Ingredients:** {', '.join(recipe_data['missing_ingredients'])}")
                
                # Check if nutrition facts should be shown
                if st.session_state.get('show_nutrition', True):  
                    st.markdown(f"**Nutrition Facts:** {recipe_data['nutrition']}")
                
                # Remove saved recipe button
                if st.button("Remove Recipe", key=f"remove_{recipe_data['title']}"):
                    st.session_state['saved_recipes'] = [r for r in st.session_state['saved_recipes'] if r['title'] != recipe_data['title']]
                    st.success(f"{recipe_data['title']} has been removed from saved recipes.")

                # Button to export saved recipes to a CSV file, shown only if a recipe is selected
                if st.button("Export to CSV"):
                    csv = convert_to_csv(st.session_state['saved_recipes'])
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name='saved_recipes.csv',
                        mime='text/csv'
                    )
        else:
            st.write("No recipe selected.")

# Left column for title and ingredient input
with col1:
    st.image("quickbite_logo.png", width=300)  # Title of the app

    # Function to clear all ingredients
    def clear_ingredients():
        st.session_state['ingredients'] = []

    # Function to add ingredient
    # Function to add ingredient
    # Function to add ingredient
    # Function to add ingredient
    # Function to add ingredient (with manual addition option)
    # Function to add ingredient (with manual addition option)
    # Function to add ingredient (adjusted to take parameters)
    # Function to add ingredient
   # Function to add ingredient
    def add_ingredient():
        ingredient_name = st.session_state['ingredient_input']
        ingredient_amount = st.session_state['amount_input']

        if not ingredient_name:  # Check if ingredient name is not empty
            st.warning("Please enter an ingredient name.")  # Show warning if name is empty
            return  # Exit early if no ingredient name

        if not ingredient_amount:  # Check if ingredient amount is provided
            st.warning("Please enter an amount for the ingredient.")  # Show warning if amount is empty
             # Exit early if no amount is provided

        # Check if ingredient already exists
        for i, (name, amount) in enumerate(st.session_state['ingredients']):
            if name.lower() == ingredient_name.lower():  # Case-insensitive comparison
                # If ingredient already exists and amount is provided, sum the amounts
                if ingredient_amount:  # Only sum if an amount is provided
                    try:
                        new_amount = str(float(amount.split()[0]) + float(ingredient_amount.split()[0])) + ' ' + ingredient_amount.split()[1]
                        st.session_state['ingredients'][i] = (name, new_amount)
                        st.success(f"Updated amount for {ingredient_name}.")  # Success message for updating ingredient
                    except ValueError:
                        st.warning("Invalid amount format. Please enter a valid number.")
                break
        else:
            # Add new ingredient if it doesn't exist
            amount_to_add = ingredient_amount if ingredient_amount else "No amount specified"  # Use a default message if no amount is provided
            st.session_state['ingredients'].append((ingredient_name, amount_to_add))
            st.success(f"{ingredient_name} added successfully!")  # Success message for adding ingredient
    
        # Clear input fields after adding the ingredient
        st.session_state['amount_input'] = ""  # Reset amount input
        st.session_state['ingredient_input'] = ""  # Reset ingredient input



    # Function to add all ingredients from session state
    def add_all_ingredients():
        for ingredient in st.session_state['ingredients']:
            add_ingredient(ingredient[0], ingredient[1])

        # Text input for ingredients
    col_input, col_amount = st.columns(2)

    with col_input:
        st.text_input(
            "Enter ingredient",
            placeholder="e.g. chicken",
            key='ingredient_input'
        )

    with col_amount:
        st.text_input(
            "Enter amount(required)",
            placeholder="e.g. 500g, 2 cups",
            key='amount_input',
            on_change=add_ingredient
        )


    if st.button("ADD INGREDIENTS"):
        for ingredient in st.session_state['ingredients']:
            add_ingredient()  # Call the function to add each ingredient

# Replace this section of your code
# Header for uploading receipt
    st.header("Upload Receipt")
    if st.button("Add Receipt"):
        st.session_state.camera_permission = True
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            if st.button("Extract Ingredients"):
                extracted_ingredients = extract_ingredients_from_image(image)
                st.session_state['ingredients'].extend(extracted_ingredients)  # Add extracted ingredients to session state
                st.success("Ingredients extracted successfully!")

    # With this secti

        # Take a picture button
        if 'camera_permission' in st.session_state and st.session_state.camera_permission:
    # Camera input
            image_file = st.camera_input("Take a picture of the receipt")

    # If a picture is taken, process it
            if image_file is not None:
                image = Image.open(image_file)
                st.image(image, caption='Captured Image', use_column_width=False, width=300)  # Adjust width as needed
                if st.button("Extract Ingredients"):
                    extracted_ingredients = extract_ingredients_from_image(image)
                    st.session_state['ingredients'].extend(extracted_ingredients)  # Add extracted ingredients to session state
                    st.success("Ingredients extracted successfully!")
        else:
            # If permission has not been granted, show a message
            st.warning("Please click 'Add Receipt' to give permission to use the camera.")



with st.sidebar:
    st.header("Current Ingredients")
    if st.session_state['ingredients']:
        # Create a list to track ingredients that should be removed
        ingredients_to_remove = []

        for i, (ingredient, amount) in enumerate(st.session_state['ingredients']):
            col_remove, col_display = st.columns([1, 4])  # Create columns for remove button and ingredient display

            with col_remove:
                # Create a button for each ingredient to remove it
                if st.button("X", key=f"remove_{ingredient}_{i}"):
                    ingredients_to_remove.append(i)  # Mark this ingredient for removal
                    
            with col_display:
                # Display the ingredient
                st.markdown(f"{ingredient} ({amount})")

        # Remove the ingredients marked for removal after displaying
        for index in reversed(ingredients_to_remove):  # Remove in reverse to avoid index issues
            st.session_state['ingredients'].pop(index)
    else:
        st.write("No ingredients added.")

# Fetch recipes button
if st.button("SEARCH RECIPES"):
    if not st.session_state['ingredients']:
        st.error("Please add ingredients before searching for recipes.")
    else:
        user_ingredients = [ingredient[0] for ingredient in st.session_state['ingredients']]
        recipes = get_recipe(user_ingredients, st.session_state.get("show_missing_ingredients_expander", True))
        if recipes is None or len(recipes) == 0:
            st.error("No recipes found. Please try again.")
        else:
            st.subheader("Recipes Found:")
            st.session_state['current_recipes'] = recipes  # Store current recipes
            for recipe in recipes:
                recipe_info = f"""
                <div style='margin: 10px 0; padding: 10px; border: 3px solid #16536b; border-radius: 5px;'>
                    <strong>{recipe['title']}</strong>
                </div>
                """
                st.markdown(recipe_info, unsafe_allow_html=True)
                recipe_details = get_recipe_details(recipe['id'])
                if recipe_details:
                    # Get instructions or default to a message
                    instructions = recipe_details.get('instructions', 'No instructions available.')
                    # Clean up HTML tags if instructions exist
                    cleaned_instructions = instructions.replace('<ol>', '').replace('</ol>', '').replace('<li>', '').replace('</li>', '') if instructions else 'No instructions available.' 
                    if st.session_state.get('show_instructions', True):  # Check if instructions should be shown
                        st.markdown(f"<p><strong>Instructions:</strong> {cleaned_instructions}</p>", unsafe_allow_html=True)
                    used_ingredients = [f"{ingredient['amount']} {ingredient['unit']} {ingredient['name']}" for ingredient in recipe['usedIngredients']]
                    st.markdown(f"<p><strong>Used Ingredients:</strong> {', '.join(used_ingredients)}</p>", unsafe_allow_html=True)
                    missing_ingredients = [f"{ingredient['amount']} {ingredient['unit']} {ingredient['name']}" for ingredient in recipe['missedIngredients']]
                    st.markdown(f"<p><strong>Missing Ingredients:</strong> {', '.join(missing_ingredients)}</p>", unsafe_allow_html=True)
                    nutrition = recipe_details.get('nutrition')
                    nutrition_info = ""
                    if nutrition:
                        nutrients = nutrition['nutrients']
                        nutrition_info = "\n".join(f"{nutrient['name']}: {nutrient['amount']} {nutrient['unit']}" for nutrient in nutrients)
                    # Check if nutrition facts should be shown
                    if st.session_state.get('show_nutrition', True):
                        st.markdown(f"<p><strong>Nutrition Facts:</strong><br>{nutrition_info}</p>", unsafe_allow_html=True)
                    
                    # Recipe data dictionary
                    recipe_data = {
                        'title': recipe['title'],
                        'instructions': cleaned_instructions,  # Use cleaned instructions here
                        'used_ingredients': used_ingredients,
                        'missing_ingredients': missing_ingredients,
                        'nutrition': nutrition_info if nutrition else 'No nutrition information available.',
                        'link': recipe_details['link'] if recipe_details['link'].startswith(('http://', 'https://')) else f"http://{recipe_details['link']}"  # Ensure the link is complete
                    }
                    
                    # Button to save the recipe using on_click
                    def save_recipe(recipe_data):
                        if recipe_data['title'] not in [r['title'] for r in st.session_state['saved_recipes']]:
                            st.session_state['saved_recipes'].append(recipe_data)
                            st.success(f"{recipe_data['title']} saved to your recipes.")
                        else:
                            st.warning(f"{recipe_data['title']} is already in your saved recipes.")
                    
                    st.button("Save Recipe", key=f"save_{recipe['id']}", on_click=save_recipe, args=(recipe_data,))

# Optional expander for additional features
with st.expander("Show Additional Features"):
    show_missing_ingredients_expander = st.checkbox("Show Recipes With Missing Ingredients", value=False, key="show_missing_ingredients_expander")
    show_instructions = st.checkbox("Show Instructions", value=True, key="show_instructions")  # Added this checkbox
    show_nutrition = st.checkbox("Show Nutrition Facts", value=True, key="show_nutrition")  # Added this checkbox
