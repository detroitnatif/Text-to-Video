from openai import OpenAI
import os
# from dotenv import load_dotenv
import narration
import json
import images
import video
import streamlit as st
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



# load_dotenv()
@st.cache_data()
def run(prompt, api_key):
    # load_dotenv()
    client = OpenAI(api_key=api_key)
    # elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")

    narration_api = 'openai'  # 'eleven_labs'

    name_response =  client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role':'system',
                    'content': ''' Your job is to read the prompt and name it using the convention of words connected by _ like these examples:
                    Example 1) Question: I want to fix my flat tire on 1998 ford focus Response: 1998_ford_focus_flat_tire
                    Example 2) Question: I want to change the sparkplugs on 2014 cadillac escalade: 2014_cadillac_escalde

                    '''
                },
                {
                    'role': 'user',
                    'content': f'Given this prompt: {prompt}, write me a name summarizing the problem that is lowercase and connected with _ '
                }
            ]

        )
    name = name_response.choices[0].message.content

    if not os.path.exists(f'{name}'):
        os.makedirs(f'{name}')
 
    response_1 =  client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role':'system',
                    'content': ''' Your job is to give the steps to solve this problem with clear and straigtforward actions that is 4 steps long . 
                    Skip the thematic answers and give as many sentences needed to make the problem 4 steps long. Before the steps, give a list all the needed materials and tools.
                    '''
                },
                {
                    'role': 'user',
                    'content': f'create a Youtube Short narration based for the following input: {prompt}, please emphasize the exact steps of the car problem: '
                }
            ]

        )
    response_recipe = response_1.choices[0].message.content

    recipe_file_path = os.path.join(name, "car_problem.txt")

    with open(recipe_file_path, "w") as file:
        file.write(response_recipe)

    with open(recipe_file_path) as f:
        source_material = f.read()

    response =  client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role':'system',
                'content': f'''You are a youtube short car problem narration generator, 
                emphasize the steps and not thematic presentation, 
                30 seconds to 1 minute narration,
                the narration you create will have a picture background for each step.
                make the numbered list as of 5 steps getting the car problem in full. 

                
                respond with the following format with 5 steps of the car problem:

                1) [Background image: all tools and parts from {source_material} laying in front of the car]

                Narrator: "list all the tools and parts from {source_material} and their respective amounts, making sure to keep this on the same line, never creating a new line between tools and parts"

                2) [Background image: Description of first step and the tools and parts involved]

                Narrator: "replace this with A few sentences of the fixing step details"

                3) [Background image: Description of second step and tools and parts involved]

                Narrator: "replace this with How to do this step of fixing with details"

                continue making the car problem in the above format for all the steps ...

                4) [Background image: Description of third step and tools and parts involved]

                Narrator: "replace this with How to do this step of fixing with details"

                5) 4) [Background image: Description of fourth step and tools and parts involved]

                Narrator: "replace this with How to do this step of fixing with details"
                '''
            },
            {
                'role':'system',
                'content': f''' below is a good example of what you should generate, but changing all the details to be the tools and parts from {source_material}:

Here are the steps and image descriptions for fixing a flat tire on a 1998 Ford Focus:

1) **[Background image: Trunk of a 1998 Ford Focus open with a spare tire, car jack, and lug wrench laid out]**

   Narrator: "Here are all the tools and parts you'll need: a spare tire, car jack, and lug wrench."

2) **[Background image: Close-up of the flat tire on the car with the lug nuts partially unscrewed]**

   Narrator: "Loosen the lug nuts on the flat tire slightly with the lug wrench while the car is still on the ground."

3) **[Background image: The car jack positioned under the car, lifting it up]**

   Narrator: "Use the car jack to lift the car until the flat tire is off the ground."

4) **[Background image: Removing the flat tire from the car]**

   Narrator: "Remove the loosened lug nuts completely, then take off the flat tire."

5) **[Background image: Installing the spare tire onto the car]**

   Narrator: "Mount the spare tire onto the wheel hub, screw the lug nuts on by hand, and then tighten them slightly with the lug wrench."

6) **[Background image: Lowering the car with the car jack and tightening the lug nuts]**

   Narrator: "Lower the car to the ground using the car jack and then tighten the lug nuts securely with the lug wrench."

7) **[Background image: The car with the newly installed spare tire, ready to drive]**

   Narrator: "Your spare tire is now installed. Check the tire pressure and drive safely to your nearest service center for a permanent solution."
                '''
            },
            {
                'role': 'user',
                'content': f'create a Youtube Short narration based on the following source material, emphasizing the exact steps of the car problem, and the first narration should be the needed tools and parts: \n\n {source_material}'
            }
        ]

    )
    response = response.choices[0].message.content

    data = narration.parse(response)
    narration.create(data, name, 'narration', api_key)

    
    with open(os.path.join(name, 'response.txt'), 'w') as f:
        f.write(response)

    with open(os.path.join(name, 'data.json'), 'w') as f:
        json.dump(data, f)

    with open(os.path.join(name, 'data.json'), 'r') as f:
        data_json = json.load(f)


    if not os.path.exists(os.path.join(name, 'images')):
        os.makedirs(os.path.join(name, 'images'))

    images.create_from_data(data, name, api_key)

    img_path = f"videoCreation/{name}/images"
    logging.info(f'{img_path}')
    # imgs_paths = sorted(os.listdir(img_path))
    fps = 30 
    mp4 = f'cooking_with_captions_{name}.mp4'
    output_dir = f'{name}'


    
    video.images_to_video(img_path, 'video_no_sound.avi', 'video.mp4', data_json, output_dir, name, fps=30)

    
    return (True, name)















# WORKING
# from openai import OpenAI
# import os
# # from dotenv import load_dotenv
# import narration
# import json
# import images
# import video
# import streamlit as st

# # load_dotenv()
# @st.cache_data()
# def run(prompt, api_key):
#     # load_dotenv()
#     client = OpenAI(api_key=api_key)
#     # elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")

#     narration_api = 'openai'  # 'eleven_labs'

#     name_response =  client.chat.completions.create(
#             model='gpt-3.5-turbo',
#             messages=[
#                 {
#                     'role':'system',
#                     'content': ''' Your job is to read the prompt and name it using the convention of words connected by _ like these examples:
#                     Example 1) Question: I want to make chinese chicken Response: chinese_chicken
#                     Example 2) Question: I want to make quiche lorraine Response: quiche_lorraine

#                     '''
#                 },
#                 {
#                     'role': 'user',
#                     'content': f'Given this prompt: {prompt}, write me a name summarizing the recipe that is lowercase and connected with _ '
#                 }
#             ]

#         )
#     name = name_response.choices[0].message.content

#     if not os.path.exists(f'{name}'):
#         os.makedirs(f'{name}')
 
#     response_1 =  client.chat.completions.create(
#             model='gpt-3.5-turbo',
#             messages=[
#                 {
#                     'role':'system',
#                     'content': ''' Your job is to give a recipe with clear and straigtforward actions that is 4 steps . 
#                     Skip the thematic answers and give as many sentences needed to make the recipe 4 steps long. Before the steps, give a list all the needed ingredients and quantities.
#                     '''
#                 },
#                 {
#                     'role': 'user',
#                     'content': f'create a Youtube Short narration based for the following input: {prompt}, please emphasize the exact steps of the recipe: '
#                 }
#             ]

#         )
#     response_recipe = response_1.choices[0].message.content

#     recipe_file_path = os.path.join(name, "recipe.txt")

#     with open(recipe_file_path, "w") as file:
#         file.write(response_recipe)

#     with open(recipe_file_path) as f:
#         source_material = f.read()

#     response =  client.chat.completions.create(
#         model='gpt-3.5-turbo',
#         messages=[
#             {
#                 'role':'system',
#                 'content': f'''You are a youtube short recipe narration generator, 
#                 emphasize the steps and not thematic presentation, 
#                 30 seconds to 1 minute narration,
#                 the narration you create will have a picture background for each step.
#                 make the numbered list as of 5 steps getting the recipe in full. 

                
#                 respond with the following format with 5 steps of the recipe:

#                 1) [Background image: all ingredients from {source_material} laying on a kitchen counter]

#                 Narrator: "list all the ingredients from {source_material} and their respective amounts, making sure to keep this on the same line, never creating a new line between ingredients"

#                 2) [Background image: Description of first step and the ingredients involved]

#                 Narrator: "replace this with A few sentences of the cooking step details"

#                 3) [Background image: Description of second step and ingredients involved]

#                 Narrator: "replace this with How to do this step of cooking with details"

#                 continue making the recipe in the above format for all the steps ...

#                 4) [Background image: Description of third step and ingredients involved]

#                 Narrator: "replace this with How to do this step of cooking with details"

#                 5) 4) [Background image: Description of fourth step and ingredients involved]

#                 Narrator: "replace this with How to do this step of cooking with details"
#                 '''
#             },
#             {
#                 'role':'system',
#                 'content': f''' below is a good example of what you should generate, but changing all the details to be the ingredients from {source_material}:


# 1)  [Background image: birds eye view of kitchen counter with ground beef, rice, onions, garlic, paprika, cumin]

# Narrator: "Here are all the ingredients you'll need: 1 pound ground beef, 2 cups rice, 3 onions , a clove of garlic, and 2 tablespoons of paprika "

# 2) [Background image: Bowl of mixed ground beef, rice, onion, garlic, and spices]

# Narrator: "Combine ground beef, rice, onion, garlic, spices to make the stuffing mixture for the cabbage rolls."

# 3) [Background image: Cabbage leaf being filled with the beef mixture]

# Narrator: "Carefully fill cabbage leaves with the beef mixture, then roll them up ensuring the sides are tucked in."

# 4) [Background image: Cabbage rolls placed in a pot with tomato sauce and diced tomatoes]

# Narrator: "Place cabbage rolls in a pot, pour over tomato sauce, diced tomatoes, season, then cover and simmer for 45-60 minutes."

# 5) [Background image: Delicious stuffed cabbage rolls ready to be served]

# Narrator: "After simmering, serve hot, and enjoy your delectable stuffed cabbage rolls!"
#                 '''
#             },
#             {
#                 'role': 'user',
#                 'content': f'create a Youtube Short narration based on the following source material, emphasizing the exact steps of the recipe, and the first narration should be the needed ingredients: \n\n {source_material}'
#             }
#         ]

#     )
#     response = response.choices[0].message.content

#     data = narration.parse(response)
#     narration.create(data, name, 'narration', api_key)

    
#     with open(os.path.join(name, 'response.txt'), 'w') as f:
#         f.write(response)

#     with open(os.path.join(name, 'data.json'), 'w') as f:
#         json.dump(data, f)

#     with open(os.path.join(name, 'data.json'), 'r') as f:
#         data_json = json.load(f)


#     if not os.path.exists(os.path.join(name, 'images')):
#         os.makedirs(os.path.join(name, 'images'))

#     images.create_from_data(data, name, api_key)

#     img_path = f"{name}/images"
#     # imgs_paths = sorted(os.listdir(img_path))
#     fps = 30 
#     mp4 = f'cooking_with_captions_{name}.mp4'
#     output_dir = f'{name}'


    
#     video.images_to_video(img_path, 'video_no_sound.avi', 'video.mp4', data_json, output_dir, name, fps=30)

#     return (True, name)



