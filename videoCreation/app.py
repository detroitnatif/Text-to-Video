import streamlit as st
from PIL import Image
import pandas as pd
import io
from io import StringIO
import os
import script



st.set_page_config(page_title='Text-to-Video')

# img = st.sidebar.selectbox(
#     "Choose an image",
#     (None, "amber.jpg", 'pizza.jpeg'),
#     )



duke_blue = "#00539B"
st.markdown(f"""
<h1 style='text-align: center; color: Black; font-size: 50px;'>RapidRecipe</h1>
<style>
    .caption-style {{
        color: grey;
        text-align: center;
    }}
    .stApp {{
        background-color: white;
    }}
    .stTextInput>div>div>input {{
        color: black !important;
        background-color: white !important;
        border-color: grey !important;
        caret-color: blue; /* Adds a blue blinking cursor */
    }}

    .stTextInput>div {{
        border-color:  {duke_blue} !important;
        border-width: 1.5px !important;
    }}
    /* Updated selector to target all buttons within Streamlit apps */
    .stButton>button {{
        display: inline-block;
        background-color: white;
        border: 2px solid #BEC2D1;;
        padding: 5px;
        margin: 2px;
        cursor: pointer;
        color: #9599B3;
        border-radius: 5px;
        width: 300px; /* Ensures equal width */
        height: 120px; /* Ensures equal height */
        text-align: center; /* Center text */
        line-height: 40px; /* Adjust line height for vertical alignment */
    }}

    
    .stButton>button:hover {{
        background-color: #f0f0f0; /* Changes background to light grey */
        color: {duke_blue}; /* Keeps the text color the same */
        border: 2px solid grey; /* Keeps the border color the same */
    }}
        .stButton {{
        margin-left: 20px !important;
    }}
    
</style>
<p class='caption-style' style='font-size: 24px; color: black;'>Create recipe videos</p>
""", unsafe_allow_html=True)

recipes = st.sidebar.selectbox(
    "Choose a recipe",
    (None, "Chinese Chicken", 'Falafel', 'Steak au Poivre')
    )

if recipes:
    formatted_recipes = recipes.lower().replace(" ", "_") + ".mp4"
    path = 'videos/' + formatted_recipes
    video_file = open(path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)



st.write("### Create your own Video")
api_key = st.text_input("Enter your OpenAI API Key:", type="password")


if len(api_key) > 40:
    requested_recipe = st.text_input(label="What would you like to eat?")

    if requested_recipe:
        recipe_name = script.run(requested_recipe, api_key)
        if recipe_name is not None:
            path = os.path.join(recipe_name, 'video.mp4')
            video_file = open(path, 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)



