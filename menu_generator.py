import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io

available_ingredient_options = [
    "Tomato", "Mozzarella Cheese", "Basil", "Olive Oil", "Chicken Breast",
    "Garlic", "Butter", "Flour", "Dark Chocolate", "Salmon Fillet", "Broccoli",
    "Carrot", "Avocado", "Rice", "Pasta", "Parmesan Cheese", "Eggs", "Lemon Juice"
]

st.set_page_config(page_title="Tasty", layout="wide")

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

def generate_menu(preferences, scaling_factor):#menu data base example
    sample_menu = [
        {
        "name": "Paneer Tikka",#dish name
        "description": "Grilled paneer marinated with spices and yogurt.",#what is the dish like
        "price": 12.0,#estimated price to make
        "category": "Vegetarian",#sub category of dish, linking to perference
        "ingredients": [#materials required to make
            {"name": "Paneer", "quantity": "200g"},
            {"name": "Yogurt", "quantity": "50g"},
            {"name": "Lemon juice", "quantity": "1 tbsp"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Spices (cumin, paprika)", "quantity": "1 tsp each"},
            {"name": "Salt", "quantity": "to taste"}
        ],
        "steps": [#steps of how this dish can be made at home
            "Marinate paneer with yogurt, lemon juice, spices, and ginger-garlic paste for 30 minutes.",
            "Grill on skewers until golden brown.",
            "Serve with mint chutney."
        ]
    },
    {
        "name": "Vegetable Lasagna",
        "description": "Layered pasta with vegetables, ricotta, and marinara sauce.",
        "price": 13.0,
        "category": "Vegetarian",
        "ingredients": [
            {"name": "Lasagna sheets", "quantity": "4"},
            {"name": "Ricotta cheese", "quantity": "150g"},
            {"name": "Spinach", "quantity": "100g"},
            {"name": "Bell peppers", "quantity": "50g"},
            {"name": "Marinara sauce", "quantity": "150ml"},
            {"name": "Mozzarella cheese", "quantity": "100g"}
        ],
        "steps": [
            "Layer cooked lasagna sheets, ricotta, spinach, vegetables, and marinara sauce.",
            "Repeat layers and top with mozzarella cheese.",
            "Bake at 180°C for 25 minutes and serve."
        ]
    },

    # Non-Vegetarian
    {
        "name": "Lamb Biryani",
        "description": "Fragrant basmati rice cooked with marinated lamb and spices.",
        "price": 20.0,
        "category": "Non-Vegetarian",
        "ingredients": [
            {"name": "Lamb", "quantity": "300g"},
            {"name": "Basmati rice", "quantity": "200g"},
            {"name": "Yogurt", "quantity": "50g"},
            {"name": "Onions", "quantity": "2 (sliced)"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Spices (cardamom, cloves, cinnamon)", "quantity": "2 tsp"}
        ],
        "steps": [
            "Marinate lamb with yogurt, spices, and ginger-garlic paste for 1 hour.",
            "Cook onions, add marinated lamb, and layer with partially cooked rice.",
            "Steam cook for 20 minutes and serve."
        ]
    },
    {
        "name": "Shrimp Scampi",
        "description": "Juicy shrimp sautéed in garlic butter and white wine sauce.",
        "price": 18.0,
        "category": "Non-Vegetarian",
        "ingredients": [
            {"name": "Shrimp", "quantity": "200g"},
            {"name": "Garlic", "quantity": "3 cloves (minced)"},
            {"name": "Butter", "quantity": "3 tbsp"},
            {"name": "White wine", "quantity": "50ml"},
            {"name": "Lemon juice", "quantity": "1 tbsp"},
            {"name": "Parsley", "quantity": "5g"}
        ],
        "steps": [
            "Melt butter and sauté garlic.",
            "Add shrimp, white wine, and lemon juice. Cook until shrimp is pink.",
            "Garnish with parsley and serve with bread or pasta."
        ]
    },

    # Salad
    {
        "name": "Greek Salad",
        "description": "A refreshing salad with cucumbers, tomatoes, feta cheese, and olives.",
        "price": 9.0,
        "category": "Salad",
        "ingredients": [
            {"name": "Cucumber", "quantity": "100g"},
            {"name": "Tomatoes", "quantity": "100g"},
            {"name": "Feta cheese", "quantity": "50g"},
            {"name": "Kalamata olives", "quantity": "30g"},
            {"name": "Olive oil", "quantity": "2 tbsp"},
            {"name": "Oregano", "quantity": "1 tsp"}
        ],
        "steps": [
            "Chop cucumbers and tomatoes into cubes.",
            "Combine with feta cheese and olives.",
            "Drizzle with olive oil and sprinkle with oregano."
        ]
    },

    # Dessert
    {
        "name": "Panna Cotta",
        "description": "Creamy Italian dessert served with berry compote.",
        "price": 8.0,
        "category": "Dessert",
        "ingredients": [
            {"name": "Heavy cream", "quantity": "200ml"},
            {"name": "Sugar", "quantity": "50g"},
            {"name": "Vanilla extract", "quantity": "1 tsp"},
            {"name": "Gelatin", "quantity": "1 tsp"},
            {"name": "Berry compote", "quantity": "50ml"}
        ],
        "steps": [
            "Heat cream, sugar, and vanilla extract until sugar dissolves.",
            "Add gelatin and mix until dissolved.",
            "Pour into molds and refrigerate for 4 hours.",
            "Serve with berry compote."
        ]
    },

    # Soup
    {
        "name": "Tom Yum Soup",
        "description": "Spicy and sour Thai soup with shrimp and mushrooms.",
        "price": 10.0,
        "category": "Soup",
        "ingredients": [
            {"name": "Shrimp", "quantity": "100g"},
            {"name": "Mushrooms", "quantity": "50g"},
            {"name": "Lemongrass", "quantity": "1 stalk"},
            {"name": "Kaffir lime leaves", "quantity": "2 leaves"},
            {"name": "Chili paste", "quantity": "1 tbsp"},
            {"name": "Fish sauce", "quantity": "1 tbsp"},
            {"name": "Lime juice", "quantity": "1 tbsp"}
        ],
        "steps": [
            "Boil water with lemongrass and kaffir lime leaves.",
            "Add mushrooms, shrimp, chili paste, fish sauce, and lime juice.",
            "Simmer for 5 minutes and serve hot."
        ]
    },

    # Appetizer
    {
        "name": "Chicken Satay",
        "description": "Grilled chicken skewers served with peanut sauce.",
        "price": 7.0,
        "category": "Appetizer",
        "ingredients": [
            {"name": "Chicken strips", "quantity": "200g"},
            {"name": "Coconut milk", "quantity": "50ml"},
            {"name": "Soy sauce", "quantity": "1 tbsp"},
            {"name": "Peanut butter", "quantity": "3 tbsp"},
            {"name": "Lime juice", "quantity": "1 tbsp"},
            {"name": "Curry powder", "quantity": "1 tsp"}
        ],
        "steps": [
            "Marinate chicken strips with coconut milk, soy sauce, and curry powder.",
            "Grill on skewers until cooked through.",
            "Serve with peanut sauce."
        ]
    },

    # Gluten-Free
    {
        "name": "Quinoa Salad",
        "description": "A healthy salad with quinoa, cherry tomatoes, cucumber, and feta.",
        "price": 10.0,
        "category": "Gluten-Free",
        "ingredients": [
            {"name": "Quinoa", "quantity": "150g"},
            {"name": "Cherry tomatoes", "quantity": "100g"},
            {"name": "Cucumber", "quantity": "100g"},
            {"name": "Feta cheese", "quantity": "50g"},
            {"name": "Olive oil", "quantity": "2 tbsp"},
            {"name": "Lemon juice", "quantity": "1 tbsp"}
        ],
        "steps": [
            "Cook quinoa and let it cool.",
            "Mix quinoa, chopped vegetables, and feta.",
            "Drizzle with olive oil and lemon juice before serving."
        ]
    },
    {
        "name": "Baked Salmon with Asparagus",
        "description": "Oven-baked salmon paired with roasted asparagus.",
        "price": 15.0,
        "category": "Gluten-Free",
        "ingredients": [
            {"name": "Salmon fillet", "quantity": "200g"},
            {"name": "Asparagus", "quantity": "100g"},
            {"name": "Olive oil", "quantity": "2 tbsp"},
            {"name": "Lemon juice", "quantity": "1 tbsp"},
            {"name": "Garlic", "quantity": "1 clove"}
        ],
        "steps": [
            "Place salmon and asparagus on a baking tray.",
            "Drizzle with olive oil, garlic, and lemon juice.",
            "Bake at 200°C for 15-20 minutes and serve hot."
        ]
    },
    {
        "name": "Beef Stroganoff",
        "description": "Creamy beef sautéed with mushrooms and served over pasta.",
        "price": 16.0,
        "category": "Non-Vegetarian",
        "ingredients": [
            {"name": "Beef strips", "quantity": "200g"},
            {"name": "Mushrooms", "quantity": "100g"},
            {"name": "Sour cream", "quantity": "50ml"},
            {"name": "Onion", "quantity": "1 (chopped)"},
            {"name": "Beef broth", "quantity": "100ml"},
            {"name": "Pasta", "quantity": "100g"}
        ],
        "steps": [
            "Sauté onions and beef strips in a pan until browned.",
            "Add mushrooms and beef broth, simmering until tender.",
            "Stir in sour cream, mix, and serve over cooked pasta."
        ]
    },
    {
        "name": "Ratatouille",
        "description": "A vibrant French vegetable stew with zucchini, tomatoes, and eggplant.",
        "price": 12.0,
        "category": "Vegetarian",
        "ingredients": [
            {"name": "Zucchini", "quantity": "100g"},
            {"name": "Tomatoes", "quantity": "150g"},
            {"name": "Eggplant", "quantity": "100g"},
            {"name": "Bell peppers", "quantity": "50g"},
            {"name": "Olive oil", "quantity": "2 tbsp"},
            {"name": "Herbs de Provence", "quantity": "1 tsp"}
        ],
        "steps": [
            "Slice zucchini, tomatoes, eggplant, and bell peppers.",
            "Layer in a baking dish, drizzle with olive oil, and season with herbs.",
            "Bake at 180°C for 40 minutes until tender."
        ]
    },
    {
        "name": "Chicken Caesar Salad",
        "description": "Grilled chicken served over crisp romaine with Caesar dressing.",
        "price": 11.0,
        "category": "Salad",
        "ingredients": [
            {"name": "Chicken breast", "quantity": "150g"},
            {"name": "Romaine lettuce", "quantity": "100g"},
            {"name": "Caesar dressing", "quantity": "2 tbsp"},
            {"name": "Parmesan cheese", "quantity": "30g"},
            {"name": "Croutons", "quantity": "50g"}
        ],
        "steps": [
            "Grill chicken breast and slice into strips.",
            "Toss romaine lettuce with Caesar dressing and croutons.",
            "Top with grilled chicken and grated Parmesan cheese."
        ]
    },
    {
        "name": "Spaghetti Carbonara",
        "description": "Classic Italian pasta with bacon, eggs, and Parmesan cheese.",
        "price": 14.0,
        "category": "Non-Vegetarian",
        "ingredients": [
            {"name": "Spaghetti", "quantity": "150g"},
            {"name": "Bacon", "quantity": "100g"},
            {"name": "Eggs", "quantity": "2"},
            {"name": "Parmesan cheese", "quantity": "50g"},
            {"name": "Black pepper", "quantity": "1 tsp"}
        ],
        "steps": [
            "Cook spaghetti and reserve pasta water.",
            "Fry bacon until crispy, then mix with spaghetti.",
            "Stir in beaten eggs and Parmesan cheese over low heat until creamy."
        ]
    },
    {
        "name": "Vegetable Stir Fry",
        "description": "Quick and healthy stir-fried vegetables with soy sauce.",
        "price": 10.0,
        "category": "Vegetarian",
        "ingredients": [
            {"name": "Broccoli", "quantity": "100g"},
            {"name": "Carrots", "quantity": "100g"},
            {"name": "Bell peppers", "quantity": "50g"},
            {"name": "Soy sauce", "quantity": "2 tbsp"},
            {"name": "Garlic", "quantity": "2 cloves (minced)"}
        ],
        "steps": [
            "Chop vegetables into bite-sized pieces.",
            "Stir fry garlic and vegetables in a wok with soy sauce.",
            "Serve hot with rice or noodles."
        ]
    },
    {
        "name": "Butter Chicken",
        "description": "Indian-style chicken cooked in a creamy tomato-based sauce.",
        "price": 17.0,
        "category": "Non-Vegetarian",
        "ingredients": [
            {"name": "Chicken breast", "quantity": "200g"},
            {"name": "Tomato puree", "quantity": "100g"},
            {"name": "Heavy cream", "quantity": "50ml"},
            {"name": "Butter", "quantity": "30g"},
            {"name": "Spices (garam masala, cumin)", "quantity": "1 tsp each"}
        ],
        "steps": [
            "Marinate chicken with spices and yogurt.",
            "Cook marinated chicken in butter until tender.",
            "Add tomato puree and heavy cream, simmer until creamy."
        ]
    },
    {
        "name": "Mushroom Risotto",
        "description": "Creamy risotto cooked with fresh mushrooms and Parmesan.",
        "price": 13.0,
        "category": "Vegetarian",
        "ingredients": [
            {"name": "Arborio rice", "quantity": "150g"},
            {"name": "Mushrooms", "quantity": "100g"},
            {"name": "Vegetable broth", "quantity": "300ml"},
            {"name": "Parmesan cheese", "quantity": "50g"},
            {"name": "Onion", "quantity": "1 (chopped)"}
        ],
        "steps": [
            "Sauté onions and mushrooms until soft.",
            "Add Arborio rice and gradually add vegetable broth while stirring.",
            "Finish with Parmesan cheese for a creamy texture."
        ]
    },
    {
        "name": "BBQ Ribs",
        "description": "Tender pork ribs slathered with smoky barbecue sauce.",
        "price": 19.0,
        "category": "Non-Vegetarian",
        "ingredients": [
            {"name": "Pork ribs", "quantity": "300g"},
            {"name": "BBQ sauce", "quantity": "100ml"},
            {"name": "Honey", "quantity": "2 tbsp"},
            {"name": "Garlic powder", "quantity": "1 tsp"}
        ],
        "steps": [
            "Marinate pork ribs with BBQ sauce, honey, and garlic powder.",
            "Bake at 180°C for 45 minutes, basting with BBQ sauce.",
            "Serve with coleslaw or cornbread."
        ]
    },
    {
        "name": "Falafel Wrap",
        "description": "Crunchy falafels wrapped in pita bread with hummus and veggies.",
        "price": 9.0,
        "category": "Vegetarian",
        "ingredients": [
            {"name": "Falafel", "quantity": "4 pieces"},
            {"name": "Pita bread", "quantity": "1"},
            {"name": "Hummus", "quantity": "2 tbsp"},
            {"name": "Cucumber", "quantity": "50g"},
            {"name": "Tomato", "quantity": "50g"}
        ],
        "steps": [
            "Spread hummus on pita bread.",
            "Add falafels, sliced cucumber, and tomato.",
            "Wrap tightly and serve."
        ]
    },
    {
        "name": "Tiramisu",
        "description": "Classic Italian dessert made with espresso-soaked ladyfingers and mascarpone.",
        "price": 9.0,
        "category": "Dessert",
        "ingredients": [
            {"name": "Ladyfingers", "quantity": "6 pieces"},
            {"name": "Mascarpone cheese", "quantity": "100g"},
            {"name": "Espresso", "quantity": "50ml"},
            {"name": "Cocoa powder", "quantity": "1 tsp"},
            {"name": "Sugar", "quantity": "30g"}
        ],
        "steps": [
            "Soak ladyfingers in espresso.",
            "Layer mascarpone mixture over soaked ladyfingers.",
            "Dust with cocoa powder and refrigerate for 2 hours before serving."
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

    # Session state initialization for ingredients
    if "available_ingredients" not in st.session_state:
        st.session_state.available_ingredients = {}

    # Dropdown list for ingredient selection
    ingredient_name = st.selectbox("Select an Ingredient", available_ingredient_options)

    # Quantity input
    quantity = st.number_input("Enter Quantity (grams/ml)", min_value=0.0, step=1.0)

    # Add selected ingredient and quantity
    if st.button("Add Ingredient"):
        if ingredient_name and quantity:
            st.session_state.available_ingredients[ingredient_name] = quantity
            st.success(f"Added {ingredient_name} ({quantity}g/ml) to your list.")
        else:
            st.warning("Please select an ingredient and enter a valid quantity.")

    # Display current ingredients
    st.write("### Your Ingredients")
    if st.session_state.available_ingredients:
        for name, qty in st.session_state.available_ingredients.items():
            st.write(f"- {name}: {qty}g/ml")
    else:
        st.info("No ingredients added yet.")

    # Generate menu button
    if st.button("Generate Menu"):
        st.session_state.generated_menu = generate_menu(
            st.session_state.preferences,
            st.session_state.scaling_factor
        )
        st.session_state.generated_menu = subtract_ingredients(
            st.session_state.generated_menu,
            st.session_state.available_ingredients
        )
        menu_items = st.session_state.generated_menu

        # Display each menu item with its details
        for item in menu_items:
            st.markdown(f"## {item['name']} - ${item['price']:.2f}")
            st.write(f"**Description:** {item['description']}")
            st.write("**Ingredients:**")
            for ingredient in item["ingredients"]:
                st.write(f"- {ingredient['name']} ({ingredient['quantity']})")

            # Add cooking steps here
            st.write("**Steps:**")
            for idx, step in enumerate(item['steps'], start=1):
                st.write(f"{idx}. {step}")

            st.write("---")

        # Generate and download menu image
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

    # "Try Again" button to go back
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
