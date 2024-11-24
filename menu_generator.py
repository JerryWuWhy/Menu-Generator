import streamlit as st
import requests
#from streamlit_lottie import st_lottie
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Tasty", layout="wide")

#def load_lottieurl(url):
    #r = requests.get(url)
    #return r.json()
#lottie_coding = "https://lottie.host/9e56d4e2-ee08-438e-a959-b76dea4f8e02/pqApA4XkmS.json"

with st.container():
    st.markdown('<p style="font-family:Impact ; font-size:60px; color:Cyan;">TASTY</p>', unsafe_allow_html=True)
    st.subheader("A menu generator that can save you!")

if "page" not in st.session_state:
    st.session_state.page = 1
if "gender" not in st.session_state:
    st.session_state.gender = None
if "age" not in st.session_state:
    st.session_state.age = None
if "job" not in st.session_state:
    st.session_state.job = None
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
    #with right_column:
        #lottie_animation = load_lottieurl(lottie_coding)
        #st_lottie(lottie_animation, height=300, key="coding")

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
            "name": "Caprese Salad",
            "description": "A simple salad with fresh mozzarella, tomatoes, and basil.",
            "price": 8.0,
            "category": "Salad",
            "ingredients": [
                {"name": "Fresh mozzarella", "quantity": "150g"},
                {"name": "Tomatoes", "quantity": "150g"},
                {"name": "Fresh basil leaves", "quantity": "10g"},
                {"name": "Olive oil", "quantity": "2 tbsp"},
                {"name": "Balsamic glaze", "quantity": "1 tbsp"},
                {"name": "Salt", "quantity": "to taste"},
                {"name": "Black pepper", "quantity": "to taste"}
            ],
            "steps": [
                "Slice the mozzarella and tomatoes into even slices.",
                "Arrange them alternately on a serving plate with basil leaves.",
                "Drizzle olive oil and balsamic glaze over the salad.",
                "Season with salt and black pepper.",
                "Serve immediately."
            ]
        },

        # Non-Vegetarian Options
        {
            "name": "Grilled Chicken Breast",
            "description": "Perfectly grilled chicken served with a side of roasted vegetables.",
            "price": 15.0,
            "category": "Non-Vegetarian",
            "ingredients": [
                {"name": "Chicken breast", "quantity": "200g"},
                {"name": "Olive oil", "quantity": "2 tbsp"},
                {"name": "Lemon juice", "quantity": "1 tbsp"},
                {"name": "Garlic", "quantity": "2 cloves"},
                {"name": "Thyme", "quantity": "1 tsp"},
                {"name": "Salt", "quantity": "to taste"},
                {"name": "Black pepper", "quantity": "to taste"}
            ],
            "steps": [
                "Marinate the chicken breast with olive oil, lemon juice, garlic, thyme, salt, and pepper for at least 30 minutes.",
                "Preheat the grill to medium-high heat.",
                "Grill the chicken for about 6-8 minutes on each side until fully cooked.",
                "Serve hot with roasted vegetables or a salad."
            ]
        },
        {
            "name": "Butter Chicken",
            "description": "A creamy, mildly spiced chicken curry with a rich tomato base.",
            "price": 18.0,
            "category": "Non-Vegetarian",
            "ingredients": [
                {"name": "Chicken (boneless)", "quantity": "250g"},
                {"name": "Tomatoes", "quantity": "200g"},
                {"name": "Cream", "quantity": "100ml"},
                {"name": "Butter", "quantity": "50g"},
                {"name": "Garlic", "quantity": "2 cloves"},
                {"name": "Ginger", "quantity": "1 inch"},
                {"name": "Garam masala", "quantity": "1 tsp"},
                {"name": "Salt", "quantity": "to taste"},
                {"name": "Cilantro", "quantity": "for garnish"}
            ],
            "steps": [
                "Heat butter in a pan and sauté garlic and ginger.",
                "Add tomatoes and cook until soft. Blend into a smooth puree.",
                "Add chicken, cream, garam masala, and salt. Simmer until chicken is cooked through.",
                "Garnish with cilantro and serve with naan or rice."
            ]
        },
        {
            "name": "Chocolate Fondant",
            "description": "Warm chocolate cake with a gooey center.",
            "price": 10.0,
            "category": "Dessert",
            "ingredients": [
                {"name": "Dark chocolate", "quantity": "150g"},
                {"name": "Butter", "quantity": "100g"},
                {"name": "Sugar", "quantity": "100g"},
                {"name": "Eggs", "quantity": "3"},
                {"name": "Flour", "quantity": "50g"}
            ],
            "steps": [
                "Melt chocolate and butter together.",
                "Whisk eggs and sugar until fluffy, then mix in the chocolate-butter mixture.",
                "Fold in the flour gently.",
                "Pour into ramekins and bake at 200°C (400°F) for 12 minutes.",
                "Serve immediately with vanilla ice cream."
            ]
        },
    
        {
            "name": "Bruschetta",
            "description": "Toasted baguette slices topped with fresh tomatoes, garlic, basil, and olive oil.",
            "price": 5.0,
            "category": "Appetizer",
            "ingredients": [
                {"name": "Baguette", "quantity": "1 (sliced into rounds)"},
                {"name": "Tomatoes", "quantity": "150g (diced)"},
                {"name": "Garlic", "quantity": "1 clove (minced)"},
                {"name": "Fresh basil", "quantity": "5g"},
                {"name": "Olive oil", "quantity": "2 tbsp"},
                {"name": "Balsamic vinegar", "quantity": "1 tsp"},
                {"name": "Salt", "quantity": "to taste"},
                {"name": "Black pepper", "quantity": "to taste"}
            ],
            "steps": [
                "Toast baguette slices in the oven until golden brown.",
                "Mix diced tomatoes, garlic, basil, olive oil, and balsamic vinegar in a bowl.",
                "Season with salt and pepper.",
                "Spoon the mixture onto the toasted baguette slices.",
                "Serve immediately."
            ]
        },
        {
            "name": "Stuffed Mushroom Caps",
            "description": "Bite-sized mushrooms filled with a cheesy garlic and herb stuffing.",
            "price": 7.0,
            "category": "Appetizer",
            "ingredients": [
                {"name": "Button mushrooms", "quantity": "12 (stems removed)"},
                {"name": "Cream cheese", "quantity": "100g"},
                {"name": "Parmesan cheese", "quantity": "50g (grated)"},
                {"name": "Garlic", "quantity": "1 clove (minced)"},
                {"name": "Parsley", "quantity": "5g (chopped)"},
                {"name": "Olive oil", "quantity": "1 tbsp"},
                {"name": "Salt", "quantity": "to taste"},
                {"name": "Black pepper", "quantity": "to taste"}
            ],
            "steps": [
                "Preheat the oven to 200°C (400°F).",
                "Mix cream cheese, Parmesan, garlic, and parsley in a bowl. Season with salt and pepper.",
                "Stuff each mushroom cap with the cheese mixture.",
                "Arrange the mushrooms on a baking tray, drizzle with olive oil.",
                "Bake for 15 minutes until the mushrooms are tender and the tops are golden.",
                "Serve warm."
            ]
        },
        {
            "name": "Zucchini Noodles with Pesto",
            "description": "Fresh zucchini noodles tossed in a vibrant basil pesto sauce.",
            "price": 9.0,
            "category": "Gluten-Free",
            "ingredients": [
                {"name": "Zucchini", "quantity": "2 medium (spiralized)"},
                {"name": "Fresh basil leaves", "quantity": "50g"},
                {"name": "Garlic", "quantity": "1 clove"},
                {"name": "Pine nuts", "quantity": "30g"},
                {"name": "Parmesan cheese", "quantity": "30g"},
                {"name": "Olive oil", "quantity": "3 tbsp"},
                {"name": "Salt", "quantity": "to taste"},
                {"name": "Black pepper", "quantity": "to taste"}
            ],
            "steps": [
                "Blend basil, garlic, pine nuts, Parmesan, olive oil, salt, and pepper to make pesto.",
                "Toss the spiralized zucchini noodles in the pesto sauce.",
                "Serve immediately, garnished with extra Parmesan and pine nuts."
            ]
        },
        {
            "name": "Grilled Lemon Herb Salmon",
            "description": "Succulent salmon fillet grilled with a zesty lemon herb marinade.",
            "price": 15.0,
            "category": "Gluten-Free",
            "ingredients": [
                {"name": "Salmon fillet", "quantity": "200g"},
                {"name": "Olive oil", "quantity": "2 tbsp"},
                {"name": "Lemon juice", "quantity": "1 tbsp"},
                {"name": "Garlic", "quantity": "1 clove (minced)"},
                {"name": "Fresh dill", "quantity": "5g (chopped)"},
                {"name": "Salt", "quantity": "to taste"},
                {"name": "Black pepper", "quantity": "to taste"}
            ],
            "steps": [
                "Preheat the grill to medium heat.",
                "Marinate the salmon with olive oil, lemon juice, garlic, dill, salt, and pepper for 15 minutes.",
                "Grill the salmon for 4-5 minutes on each side, until flaky and cooked through.",
                "Serve with a side of steamed vegetables or salad."
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
        for item in menu_items:
            st.markdown(f"**{item['name']}** - ${item['price']:.2f}")
            st.write(f"Description: {item['description']}")
            st.write("Ingredients:")
            for ingredient in item["ingredients"]:
                st.write(f"- {ingredient['name']} ({ingredient['quantity']})")
            st.write("---")

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
    def go_back_page_4():
        st.session_state.page = 4

    st.button("Try Again", on_click=go_back_page_4)
        
def page_a():
    st.title("Welcome to Tasty!")
    st.write("Start by selecting your gender.")
    st.session_state.gender = st.radio("Select your gender:", ["Male", "Female", "Other"])

    def go_to_page_2():
        st.session_state.page = 2

    st.button("Next", on_click=go_to_page_2)

def page_b():
    st.title("Step 2: Age Selection")
    st.write("Select your age range.")
    st.session_state.age = st.slider("Age:", 18, 100, 25)

    def go_to_page_3():
        st.session_state.page = 3

    st.button("Next!", on_click=go_to_page_3)

def page_c():
    st.title("Step 3: Job Selection")
    st.write("Tell us about your job.")
    st.session_state.job = st.selectbox("Select your job:", ["Student", "Engineer", "Designer", "Doctor", "Other"])

    
    def go_to_page_4():
        st.session_state.page = 4

    st.button("Next!!", on_click=go_to_page_4)
    

def summary_page():
    st.title("Summary of Inputs")
    st.write(f"**Gender:** {st.session_state.gender}")
    st.write(f"**Age:** {st.session_state.age}")
    st.write(f"**Job:** {st.session_state.job}")

    scaling_factor = get_scaling_factor(
    st.session_state.age, st.session_state.gender, st.session_state.job
)
    st.header("Preferences Input")
    preferences = st.multiselect(
    "Select your preferences",
    [
            "Vegetarian",
            "Non-Vegetarian",
            "Salad",
            "Dessert",
            "Soup",
            "Appetizer",
            "Gluten-Free"
    ]
)

    def go_to_page_5():
        st.session_state.page = 5
        st.session_state.preferences = preferences
        st.session_state.scaling_factor = scaling_factor

    st.button("Next!!!", on_click=go_to_page_5)

if st.session_state.page == 1:
    page_a()
elif st.session_state.page == 2:
    page_b()
elif st.session_state.page == 3:
    page_c()
elif st.session_state.page == 4:
    summary_page()
elif st.session_state.page == 5:
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
