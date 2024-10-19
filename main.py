import streamlit as st
import pandas as pd
from PIL import Image
import requests
import io

# Set the page configuration
st.set_page_config(page_title="Recipe Finder", layout="wide")

# Initialize session state for ingredients and dynamic keys if they don't exist
if 'ingredients' not in st.session_state:
    st.session_state['ingredients'] = []
if 'ingredient_key' not in st.session_state:
    st.session_state['ingredient_key'] = 0  # Dynamic key for ingredient input
if 'amount_key' not in st.session_state:
    st.session_state['amount_key'] = 0  # Dynamic key for amount input
if 'show_uploader' not in st.session_state:
    st.session_state['show_uploader'] = False  # Flag to toggle uploader visibility

# Spoonacular API Key (replace 'your_api_key' with your actual API key)
spoonacular_api_key = "1e489973c24e437b92a3571cb5ef0e18"

# Function to add an ingredient and reset input
def add_ingredient():
    ingredient = st.session_state.get(f'ingredient_input_{st.session_state["ingredient_key"]}', '')
    amount = st.session_state.get(f'amount_input_{st.session_state["amount_key"]}', '')
    
    if ingredient:  # Only add if the input is not empty
        if amount:
            st.session_state['ingredients'].append(f"{ingredient} ({amount})")  # Add the amount in parentheses
        else:
            st.session_state['ingredients'].append(ingredient)

        # Reset input by incrementing the dynamic key to refresh the input fields
        st.session_state['ingredient_key'] += 1
        st.session_state['amount_key'] += 1

        # Display confirmation message
        st.write("Ingredients added to the list.")  # This displays the confirmation message after adding ingredients


# Function to clear all ingredients
def clear_ingredients():
    st.session_state['ingredients'] = []  # Reset the ingredients list

# Function to detect the ingredient from an uploaded image using Spoonacular API
def detect_ingredient(image):
    api_url = f"https://api.spoonacular.com/food/images/analyze?apiKey={spoonacular_api_key}"
    response = requests.post(api_url, files={"file": image})
    
    if response.status_code == 200:
        return response.json().get("category", "Unknown ingredient")
    return "Error detecting ingredient"

# Function to simulate fetching recipes based on ingredients
def get_recipe(ingredients):
    api_url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={spoonacular_api_key}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.json()  # Assuming the API returns a list of recipes
    return None

# Function to simulate fetching recipe details
def get_recipe_details(recipe_id):
    api_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={spoonacular_api_key}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.json()
    return None

# Function to handle form submission manually, ensuring everything works on the first click
def submit_ingredient_form():
    # Call add_ingredient when the form is submitted
    add_ingredient()

# Sidebar on the right
with st.sidebar:
    st.header("Saved Recipes")
    with st.expander("View Saved Recipes"):
        # Button to export saved recipes to a CSV file
        if st.button("Export to CSV"):
            csv = pd.DataFrame(st.session_state['ingredients']).to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='saved_recipes.csv',
                mime='text/csv'
            )

    # Button to clear all ingredients
    if st.button("Clear All Ingredients"):
        clear_ingredients()

<<<<<<< HEAD
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
st.image("quickbite_logo.png", width=300)
if st.button("SEARCH RECIPES"):
    if not st.session_state['ingredients']:
        st.error("Please add ingredients before searching for recipes.")
=======
    # Display the list of ingredients
    st.header("Current Ingredients")
    if st.session_state['ingredients']:
        st.markdown("\n".join(f"- {ingredient}" for ingredient in st.session_state['ingredients']))
>>>>>>> fc2c2fe587ef968fa9bdab6265d63e155f93c478
    else:
        st.write("No ingredients added.")

# Main section for input and recipe fetching
st.header("QUICKBITE")

# Use a form to handle submission only when Enter is pressed, not when clicking outside
with st.form("ingredient_form", clear_on_submit=True):
    # Two columns: one for ingredient and one for amount
    ingredient_col, amount_col = st.columns([2, 1])

    # Ingredient input field with dynamic key to reset on each addition
    with ingredient_col:
        ingredient = st.text_input(
            "Enter your ingredient",
            placeholder="e.g. chicken, rice",
            key=f'ingredient_input_{st.session_state["ingredient_key"]}'  # Dynamic key for ingredient input
        )

    # Amount input field with dynamic key to reset on each addition
    with amount_col:
        amount = st.text_input(
            "Amount (optional)",
            placeholder="e.g. 200g, 2 cups",
            key=f'amount_input_{st.session_state["amount_key"]}'  # Dynamic key for amount input
        )

    # Submit button within the form triggers "Enter" key
    submitted = st.form_submit_button("Add Ingredients", on_click=submit_ingredient_form)

# Dropdown for additional options (checkboxes)
with st.expander("Select Additional Features"):
    show_missing_ingredients = st.checkbox("Show missing ingredients with available recipes")
    show_instructions = st.checkbox("Show recipe instructions")
    show_nutrition = st.checkbox("Show nutrition facts")
    show_prices = st.checkbox("Show estimated prices for the missing ingredients")


# Upload Photo button
if st.button("Upload Photo"):
    st.session_state['show_uploader'] = True  # Show the file uploader when the button is clicked


# Function to detect ingredients from a receipt image using Spoonacular API
def detect_ingredients_from_receipt(image):
    api_url = f"https://api.spoonacular.com/food/products/detect?apiKey={spoonacular_api_key}"  # Spoonacular endpoint for detecting from receipts
    response = requests.post(api_url, files={"file": image})
    
    if response.status_code == 200:
        # Extract ingredient names from the detected products
        products = response.json().get("products", [])
        return [product['title'] for product in products]
    return []

# Upload Photo button
if st.button("Upload Receipt"):
    st.session_state['show_uploader'] = True  # Show the file uploader when the button is clicked

# Display file uploader and process the image without showing it
if st.session_state['show_uploader']:
    uploaded_image = st.file_uploader("Upload an image of a receipt", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        img_bytes = io.BytesIO()
        image = Image.open(uploaded_image)
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Call the Spoonacular API to detect ingredients from the receipt
        detected_ingredients = detect_ingredients_from_receipt(img_bytes)

        if detected_ingredients:
            st.write(f"Detected Ingredients: {', '.join(detected_ingredients)}")
            # Optionally add detected ingredients to the ingredients list
            st.session_state['ingredients'].extend(detected_ingredients)
            st.write("Ingredients from receipt added to the list.")
        else:
            st.write("No ingredients detected from the receipt.")


# Display file uploader and process the image without showing it
if st.session_state['show_uploader']:
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_image:
        img_bytes = io.BytesIO()
        image = Image.open(uploaded_image)
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        # Call the backend API or detection function
        detected_ingredient = detect_ingredient(img_bytes)
        st.write(f"Detected Ingredient: **{detected_ingredient}**")

        # Optional: Allow the user to add the detected ingredient
        if st.button("Add Detected Ingredient"):
            st.session_state['ingredients'].append(detected_ingredient)



# Fetch Recipes button
if st.button("FETCH RECIPES"):
    if st.session_state['ingredients']:
        user_ingredients = ", ".join(st.session_state['ingredients'])
        st.header("Recipes Based on Your Ingredients")

        # Simulating fetching recipes based on the ingredients
        recipes = get_recipe(user_ingredients)  # Use actual API in production

        # Check if recipes is None and handle the error
        if recipes is None:
            st.error("Error fetching recipes. Please try again.")
        else:
            st.subheader("Recipes Found:")

            # Display the recipe results inside the square container
            for recipe in recipes:  # Assuming 'recipes' is a list of recipe details
                st.markdown(f"<div style='margin: 5px; text-align: left;'><strong>{recipe['title']}</strong></div>", unsafe_allow_html=True)

                # Fetch and display detailed recipe information
                recipe_details = get_recipe_details(recipe['id'])  # Fetch detailed recipe information
                if recipe_details:
                    # Display cooking instructions
                    instructions = recipe_details.get('instructions', 'No instructions available.')
                    st.markdown(f"<p><strong>Instructions:</strong> {instructions}</p>", unsafe_allow_html=True)

                    # Safely handle 'usedIngredients' and 'missedIngredients'
                    used_ingredients = recipe_details.get('usedIngredients', [])
                    if used_ingredients:
                        used_ingredient_names = [ingredient['name'] for ingredient in used_ingredients]
                        st.markdown(f"<p><strong>Used Ingredients:</strong> {', '.join(used_ingredient_names)}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p><strong>Used Ingredients:</strong> Not available</p>", unsafe_allow_html=True)

                    missed_ingredients = recipe_details.get('missedIngredients', [])
                    if missed_ingredients:
                        missed_ingredient_names = [ingredient['name'] for ingredient in missed_ingredients]
                        st.markdown(f"<p><strong>Missing Ingredients:</strong> {', '.join(missed_ingredient_names)}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p><strong>Missing Ingredients:</strong> Not available</p>", unsafe_allow_html=True)

                    # Display nutrition facts if available
                    nutrition = recipe_details.get('nutrition')
                    if nutrition:
                        nutrients = nutrition.get('nutrients', [])
                        if nutrients:
                            nutrition_info = "\n".join(f"{nutrient['name']}: {nutrient['amount']} {nutrient['unit']}" for nutrient in nutrients)
                            st.markdown(f"<p><strong>Nutrition Facts:</strong><br>{nutrition_info}</p>", unsafe_allow_html=True)

                    # Link to the recipe
                    st.markdown(f"[View Full Recipe](https://spoonacular.com/recipes/{recipe['id']})", unsafe_allow_html=True)
    else:
        st.warning("Please add at least one ingredient to fetch recipes.")
