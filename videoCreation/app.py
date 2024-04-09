import streamlit as st
from PIL import Image
import pandas as pd
import io
from io import StringIO
import os
import script
from time import sleep

st.set_page_config(page_title='Text-to-Video', page_icon='🎥')
base_path = os.environ.get('OPENAI_SANDBOX_BASE_PATH', '')

duke_blue = "#00539B"
st.markdown(f"""
<h1 style='text-align: center; color: Black; font-size: 50px;'>RapidRecipe</h1>
<style>
    /* Existing styles */
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
    .stButton>button {{
        display: inline-block;
        background-color: white;
        border: 2px solid #BEC2D1;
        padding: 5px;
        margin: 2px;
        cursor: pointer;
        color: #9599B3;
        border-radius: 5px;
        width: 300px;
        height: 120px;
        text-align: center;
        line-height: 40px;
    }}

    .stButton>button:hover {{
        background-color: #f0f0f0;
        color: {duke_blue};
        border: 2px solid grey;
    }}
    .stButton {{
        margin-left: 20px !important;
    }}
    .stVideo {{
        margin-left: 20px !important;
        height: 600px;
    }}
    .stTextInput label {{
        color: black !important;
    }}

    /* Custom CSS for changing password widget color */
    .stTextInput input[type="password"] {{
        color: blue !important;
    }}

    /* Change sidebar background color */
    .css-1aumxhk {{
        background-image: linear-gradient({duke_blue}, {duke_blue});
        color: white;
    }}

</style>
<p class='caption-style' style='font-size: 24px; color: black;'>Create recipe videos using OpenAI</p>
""", unsafe_allow_html=True)


# Placeholders for later use
video_placeholder = st.empty()
download_placeholder = st.empty()


recipes = st.sidebar.selectbox(
    "Choose a generated recipe, or create your own!",
    (None, "Stuffed Cabbage", "Indian Butter Chicken", "Fajitas", "Chinese Chicken", 'Falafel', 'Steak au Poivre')
)

if recipes:
    current_dir = os.getcwd()
    formatted_recipes = recipes.lower().replace(" ", "_") + ".mp4"
    path = os.path.join(current_dir, 'videoCreation/videos', formatted_recipes)
    video_file = open(path, 'rb')
    video_bytes = video_file.read()
    video_placeholder.video(video_bytes)
    
    download_placeholder.download_button(label="Download Video",
                       data=video_bytes,
                       file_name=formatted_recipes,
                       mime='video/mp4',
                       key='download_video_recipes')

# create_video_placeholder.markdown("<h3 style='color: black;'>Create your own Video</h3>", unsafe_allow_html=True)
# Now placing the API key input at the bottom
api_key = st.text_input("Enter your OpenAI API Key:")

if len(api_key) > 40:
    requested_recipe = st.text_input(label="What would you like to eat?")

    if requested_recipe:
            loading_message = st.empty() 
            loading_message.markdown("<h3 style='color: black;'>Your video is in the oven...</h3>", unsafe_allow_html=True)
            try:
                success, recipe_name = script.run(requested_recipe, api_key)
            except Exception as e:
                 st.error("Try requesting again. all the chefs are busy")
            if success:
                # if recipe_name is not None:
                path = os.path.join(recipe_name, 'video.mp4')
                video_file = open(path, 'rb')
                video_bytes = video_file.read()
                
                loading_message.empty()  
                
              
                with open(path, 'rb') as video_file:
                    video_bytes = video_file.read()
                video_placeholder.video(video_bytes)

                download_placeholder.download_button(label="Download Video",
                                   data=video_bytes,
                                   file_name=f"{recipe_name}.mp4",
                                   mime='video/mp4',
                                    key='download_video_recipes')