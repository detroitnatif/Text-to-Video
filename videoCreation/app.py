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
    script.run(requested_recipe)
# if requested_recipe is not None:
   
#     input_image = Image.open(uploaded_file)
#     input_image = input_image.resize((256, 256), Image.Resampling.LANCZOS)
#     st.image(input_image, caption='Uploaded Image.', use_column_width=True, width=200)
#     output_image = "../images/output-images/" + style_name + "-" + uploaded_file.name

# model = '../saved_models/' + style_name + ".pth"
# st.write(model)

# clicked = st.button("# Stylize Image")

# if clicked:
    
#     model = script.load_model(model)
#     style.stylize(model, input_image, output_image)
#     st.write("### Output Image:")
#     styled_image = Image.open(output_image)
#     st.image(styled_image, width=400)

