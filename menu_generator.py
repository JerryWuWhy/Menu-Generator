import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Tasty", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    return r.json()
lottie_coding = "https://lottie.host/9e56d4e2-ee08-438e-a959-b76dea4f8e02/pqApA4XkmS.json"
with st.container():
    st.markdown('<p style="font-family:Impact ; font-size:60px; color:Cyan;">TASTY</p>', unsafe_allow_html=True)
    st.subheader("A menu generator that can save you!")
    
if "page" not in st.session_state:
    st.session_state.page = "main"
if "generated_menu" not in st.session_state:
    st.session_state.generated_menu = []
if "available_ingredients" not in st.session_state:
    st.session_state.available_ingredients = {}
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What is this website?")
        st.write(
            """
            Tasty is an functional website that can:
            - generate a suitable menu
            - customized by the user's perference
            - allow different types of food styles
            - list out the food required to purchase
            - and enjoy the fun of cooking!
            """
        )
    st.markdown("---")
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")
def get_scaling_factor(age, gender, job):
    scaling_factor = 1.0
    if gender == "Male":
        scaling_factor *= 1.2
    elif gender == "Female":
        scaling_factor *= 0.9

    if age < 30:
        scaling_factor *= 1.1
    elif age > 50:
        scaling_factor *= 0.9

    if job in ["Engineer", "Doctor"]:
        scaling_factor *= 1.2
    elif job in ["Student", "Designer"]:
        scaling_factor *= 0.8

    return scaling_factor

def adjust_ingredient_quantities(ingredients, scaling_factor):
    adjusted_ingredients = []
    for ingredient in ingredients:
        if 'g' in ingredient['quantity']:
            base_quantity = float(ingredient['quantity'].replace('g', '').strip())
            adjusted_quantity = base_quantity * scaling_factor
            adjusted_ingredients.append(
                {"name": ingredient['name'], "quantity": f"{adjusted_quantity:.1f}g"}
            )
        elif 'ml' in ingredient['quantity']:
            base_quantity = float(ingredient['quantity'].replace('ml', '').strip())
            adjusted_quantity = base_quantity * scaling_factor
            adjusted_ingredients.append(
                {"name": ingredient['name'], "quantity": f"{adjusted_quantity:.1f}ml"}
            )
        else:
            adjusted_ingredients.append(ingredient)
    return adjusted_ingredients

def generate_menu(preferences, scaling_factor):
    
    sample_menu = [
        {
            "name": "Margherita Pizza",
            "description": "Classic pizza with tomatoes, mozzarella, and basil",
            "price": 10.0,
            "category": "Vegetarian",
            "ingredients": [
                {"name": "Pizza dough", "quantity": "250g"},
                {"name": "Tomato sauce", "quantity": "100g"},
                {"name": "Mozzarella cheese", "quantity": "150g"},
                {"name": "Fresh basil leaves", "quantity": "10g"},
                {"name": "Olive oil", "quantity": "2 tbsp"},
                {"name": "Salt", "quantity": "to taste"},
                {"name": "Black pepper", "quantity": "to taste"}
            ],
            "steps": [
                "Preheat the oven to 250°C (475°F).",
                "Roll out the pizza dough and place it on a baking sheet.",
                "Spread tomato sauce evenly over the dough.",
                "Sprinkle mozzarella cheese over the sauce.",
                "Season with salt and black pepper.",
                "Bake in the preheated oven for about 10-12 minutes, until the cheese is melted and slightly golden.",
                "Remove from oven, add fresh basil leaves, and lightly brush with olive oil.",
                "Slice and serve."
            ]
        },
        {
            "name": "Sushi Roll",
            "description": "Traditional Japanese sushi with fresh fish and vegetables",
            "price": 18.0,
            "category": "Non-Vegetarian",
            "ingredients": [
                {"name": "Sushi rice", "quantity": "200g"},
                {"name": "Nori (seaweed)", "quantity": "2 sheets"},
                {"name": "Fresh fish (tuna, salmon)", "quantity": "150g"},
                {"name": "Cucumber", "quantity": "50g"},
                {"name": "Avocado", "quantity": "50g"},
                {"name": "Soy sauce", "quantity": "50ml"},
                {"name": "Wasabi", "quantity": "to taste"},
                {"name": "Pickled ginger", "quantity": "to taste"}
            ],
            "steps": [
                "Cook the sushi rice according to package instructions and let it cool.",
                "Lay a sheet of nori on a sushi mat, and spread rice evenly over the nori.",
                "Place slices of fish, cucumber, and avocado in the center.",
                "Roll the sushi tightly using the mat and cut into bite-sized pieces.",
                "Serve with soy sauce, wasabi, and pickled ginger."
            ]
        },
        {
            "name": "Vegetable Stir-Fry",
            "description": "Quick stir-fried vegetables with soy sauce and garlic",
            "price": 9.0,
            "category": "Vegetarian",
            "ingredients": [
                {"name": "Broccoli", "quantity": "150g"},
                {"name": "Carrots", "quantity": "100g"},
                {"name": "Bell peppers", "quantity": "100g"},
                {"name": "Snow peas", "quantity": "50g"},
                {"name": "Garlic", "quantity": "2 cloves"},
                {"name": "Soy sauce", "quantity": "30ml"},
                {"name": "Olive oil", "quantity": "2 tbsp"}
            ],
            "steps": [
                "Heat olive oil in a wok or large pan.",
                "Add minced garlic and sauté for a minute.",
                "Add chopped vegetables and stir-fry for 5-7 minutes.",
                "Pour in soy sauce and cook for another 2 minutes until vegetables are tender.",
                "Serve over rice or noodles."
            ]
        },
        {
            "name": "Fish Tacos",
            "description": "Grilled fish tacos with cabbage slaw and avocado",
            "price": 14.0,
            "category": "Non-Vegetarian",
            "ingredients": [
                {"name": "White fish (tilapia, cod)", "quantity": "200g"},
                {"name": "Taco tortillas", "quantity": "4 pieces"},
                {"name": "Cabbage slaw", "quantity": "100g"},
                {"name": "Avocado slices", "quantity": "50g"},
                {"name": "Lime", "quantity": "1 lime"},
                {"name": "Cilantro", "quantity": "10g"},
                {"name": "Sour cream", "quantity": "2 tbsp"},
                {"name": "Salt", "quantity": "to taste"}
            ],
            "steps": [
                "Grill the fish with a pinch of salt and lime juice until cooked through.",
                "Assemble the tacos with grilled fish, cabbage slaw, avocado slices, and cilantro.",
                "Top with a dollop of sour cream and serve with lime wedges."
            ]
        },
        {
            "name": "Mango Sticky Rice",
            "description": "Traditional Thai dessert with coconut milk and fresh mango",
            "price": 7.0,
            "category": "Dessert",
            "ingredients": [
                {"name": "Sticky rice", "quantity": "150g"},
                {"name": "Coconut milk", "quantity": "100ml"},
                {"name": "Sugar", "quantity": "50g"},
                {"name": "Salt", "quantity": "to taste"},
                {"name": "Fresh mango slices", "quantity": "100g"}
            ],
            "steps": [
                "Cook the sticky rice according to package instructions.",
                "In a saucepan, heat coconut milk, sugar, and salt until combined, then pour over the cooked sticky rice.",
                "Let the rice absorb the coconut milk for 10 minutes.",
                "Serve with fresh mango slices on the side."
            ]
        },
        {
            "name": "Banana Bread",
            "description": "Moist banana bread with walnuts",
            "price": 6.0,
            "category": "Dessert",
            "ingredients": [
                {"name": "Ripe bananas", "quantity": "3 medium bananas"},
                {"name": "Flour", "quantity": "250g"},
                {"name": "Sugar", "quantity": "150g"},
                {"name": "Butter", "quantity": "100g"},
                {"name": "Eggs", "quantity": "2 large"},
                {"name": "Baking powder", "quantity": "1 tsp"},
                {"name": "Salt", "quantity": "1/2 tsp"},
                {"name": "Walnuts", "quantity": "50g"}
            ],
            "steps": [
                "Preheat the oven to 180°C (350°F). Grease a loaf pan.",
                "Mash the bananas in a bowl and mix with melted butter, sugar, eggs, and vanilla extract.",
                "In a separate bowl, mix flour, baking powder, and salt.",
                "Combine the wet and dry ingredients, and fold in the walnuts.",
                "Pour the batter into the prepared pan and bake for 50-60 minutes.",
                "Let cool before serving."
            ]
        }
    ]
    filtered_menu = [item for item in sample_menu if item['category'] in preferences]
    for item in filtered_menu:
        item['ingredients'] = adjust_ingredient_quantities(item['ingredients'], scaling_factor)
    return filtered_menu

def subtract_ingredients(menu, available_ingredients):
    updated_menu = []
    for item in menu:
        updated_ingredients = []
        for ingredient in item['ingredients']:
            ingredient_name = ingredient['name']
            quantity = ingredient['quantity']

            if ingredient_name in available_ingredients:
                available_quantity = available_ingredients[ingredient_name]

                # Parse the quantity from the ingredient
                if 'g' in quantity:
                    required_quantity = float(quantity.replace('g', '').strip())
                    remaining_quantity = required_quantity - available_quantity
                    if remaining_quantity > 0:
                        updated_ingredients.append({"name": ingredient_name, "quantity": f"{remaining_quantity:.1f}g"})
                elif 'ml' in quantity:
                    required_quantity = float(quantity.replace('ml', '').strip())
                    remaining_quantity = required_quantity - available_quantity
                    if remaining_quantity > 0:
                        updated_ingredients.append({"name": ingredient_name, "quantity": f"{remaining_quantity:.1f}ml"})
                else:
                    updated_ingredients.append(ingredient)
            else:
                updated_ingredients.append(ingredient)

        item['ingredients'] = updated_ingredients
        updated_menu.append(item)

    return updated_menu

def create_menu_image(menu_items):
    img = Image.new('RGB', (800, 1200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    y_offset = 20
    d.text((20, y_offset), "Generated Menu", fill=(0, 0, 0), font=font)
    y_offset += 40

    for index, item in enumerate(menu_items, start=1):
        d.text((20, y_offset), f"{index}. {item['name']} - ${item['price']:.2f}", fill=(0, 0, 0), font=font)
        y_offset += 30
        d.text((40, y_offset), f"Description: {item['description']}", fill=(0, 0, 0), font=font)
        y_offset += 30
        d.text((40, y_offset), f"Category: {item['category']}", fill=(0, 0, 0), font=font)
        y_offset += 30
        d.text((40, y_offset), "Ingredients:", fill=(0, 0, 0), font=font)
        y_offset += 30
        for ingredient in item['ingredients']:
            d.text((60, y_offset), f"- {ingredient['name']} ({ingredient['quantity']})", fill=(0, 0, 0), font=font)
            y_offset += 20
        y_offset += 40
        d.text((40, y_offset), "Steps:", fill=(0, 0, 0), font=font)
        y_offset += 30
        for step in item['steps']:
            d.text((60, y_offset), f"- {step}", fill=(0, 0, 0), font=font)
            y_offset += 20
        y_offset += 40

    return img

def main_page():
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if username == "admin" and password == "password":
            st.sidebar.success("Logged in as {}".format(username))
    
    gender = st.sidebar.selectbox("Select your gender", ["Male", "Female", "Other"])
    age = st.sidebar.slider("Select your age", 18, 100, 25)
    job = st.sidebar.selectbox("Select your job", ["Student", "Engineer", "Designer", "Doctor", "Other"])
    scaling_factor = get_scaling_factor(age, gender, job)
    
    st.header("Preferences Input")
    preferences = st.multiselect("Select your preferences", ["Vegetarian", "Non-Vegetarian", "Salad", "Dessert"])
    st.write(f"Gender: {gender}")
    st.write(f"Age: {age}")
    st.write(f"Job: {job}")

    if st.button("Next Step"):
        st.session_state.page = "page2"
        st.session_state.preferences = preferences
        st.session_state.scaling_factor = scaling_factor

def page_2():
    st.title("Select Ingredients You Already Have")
    ingredient_name = st.text_input("Ingredient Name")
    quantity = st.number_input("Quantity (grams/ml)", min_value=0.0, step=1.0)
    
    if st.button("Add Ingredient"):
        if ingredient_name and quantity:
            st.session_state.available_ingredients[ingredient_name] = quantity
            st.success(f"Added {ingredient_name} ({quantity}g/ml) to your list.")

    st.write("### Your Ingredients")
    if st.session_state.available_ingredients:
        for name, qty in st.session_state.available_ingredients.items():
            st.write(f"- {name}: {qty}g/ml")

    if st.button("Generate Menu"):
        st.session_state.generated_menu = generate_menu(st.session_state.preferences, st.session_state.scaling_factor)
        st.session_state.generated_menu = subtract_ingredients(st.session_state.generated_menu, st.session_state.available_ingredients)
        
        menu_items = st.session_state.generated_menu
        for index, item in enumerate(menu_items, start=1):
            st.text(f"{index}. {item['name']}")
            st.text(f"   Description: {item['description']}")
            st.text(f"   Price: ${item['price']:.2f}")
            st.text(f"   Category: {item['category']}")
            st.text("   Ingredients:")
            for ingredient in item['ingredients']:
                st.text(f"      - {ingredient['name']} ({ingredient['quantity']})")
            st.text("   Steps:")
            for step in item['steps']:
                st.text(f"      - {step}")
            st.text("\n" + "-"*50 + "\n")

        img = create_menu_image(menu_items)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        st.download_button(
            label="Save Menu as JPEG",
            data=buffer,
            file_name="generated_menu.jpg",
            mime="image/jpeg"
        )
    if st.button("Go back to Main Page"):
        st.session_state.page = "main"

if st.session_state.page == 'main':
    main_page()
elif st.session_state.page == 'page2':
    page_2()

st.markdown("---")
st.header("Contact Us")
email = st.text_input("Your email address")
if st.button("Submit"):
    if email:
        st.success(f"Thank you! We will contact you at {email}.")
    else:
        st.error("Please enter a valid email address.")
# Run the Streamlit: source ~/.bash_profile
