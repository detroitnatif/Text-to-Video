import streamlit as st
from PIL import Image
import pandas as pd
import io
from io import StringIO
import os
import script

st.title("Text-to-Recipe")

# img = st.sidebar.selectbox(
#     "Choose an image",
#     (None, "amber.jpg", 'pizza.jpeg'),
#     )

recipes = st.sidebar.selectbox(
    "Choose a recipe",
    (None, "Chinese Chicken", 'Quiche Lorraine', 'Steak au Poivre')
    )

if recipes:
    formatted_recipes = recipes.lower().replace(" ", "_") + ".mp4"
    path = 'videos/' + formatted_recipes
    video_file = open(path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)



st.write("### Create your own Video")
requested_recipe = st.text_input(label="What would you like to eat?")

if requested_recipe:
    recipe_name = script.run(requested_recipe)
    if recipe_name is not None:
        path = os.path.join(recipe_name, 'video.mp4')
        video_file = open(path, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
# st.write(model)

# clicked = st.button("# Stylize Image")

# if clicked:
    
#     model = script.load_model(model)
#     style.stylize(model, input_image, output_image)
#     st.write("### Output Image:")
#     styled_image = Image.open(output_image)
#     st.image(styled_image, width=400)

