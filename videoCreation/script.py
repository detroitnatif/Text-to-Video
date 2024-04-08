from openai import OpenAI
import os
# from dotenv import load_dotenv
import narration
import json
import images
import video


# load_dotenv()

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
                    Example 1) Question: I want to make chinese chicken Response: chinese_chicken
                    Example 2) Question: I want to make quiche lorraine Response: quiche_lorraine

                    '''
                },
                {
                    'role': 'user',
                    'content': f'Given this prompt: {prompt}, write me a name summarizing the recipe that is lowercase and connected with _ '
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
                    'content': ''' Your job is to give recipe with clear and straigtforward steps. 
                    Skip the thematic answers and give as many numbered steps as needed of about 2 sentences each. Before the steps, give a list all the needed ingredients and quantities.
                    '''
                },
                {
                    'role': 'user',
                    'content': f'create a Youtube Short narration based for the following input: {prompt}, please emphasize the exact steps of the recipe: '
                }
            ]

        )
    response_recipe = response_1.choices[0].message.content

    recipe_file_path = os.path.join(name, "recipe.txt")

    with open(recipe_file_path, "w") as file:
        file.write(response_recipe)

    with open(recipe_file_path) as f:
        source_material = f.read()

    response =  client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role':'system',
                'content': f'''You are a youtube short recipe narration generator, 
                emphasize the steps and not thematic presentation, 
                30 seconds to 1 minute narration,
                the narration you create will have a picture background for each step.
                make the numbered list as of 5 steps getting the recipe in full. 

                
                respond with the following format with however many steps of the recipe:

                1) [Background image: all ingredients from {source_material} laying on a kitchen counter]

                Narrator: "list all the ingredients from {source_material} and their respective amounts, making sure to keep this on the same line, never creating a new line between ingredients"

                2) [Background image: Description of image first Ingredient and step]

                Narrator: "replace this with A few sentences of the cooking step details"

                3) [Background image: Description of image second Ingredient and step]

                Narrator: "replace this with How to do this step of cooking with details"

                continue making the recipe in the above format for all the steps ...

                4) [Background image: Description of image 3rd Ingredient and step]

                Narrator: "replace this with How to do this step of cooking with details"

                5) 4) [Background image: Description of image 4th Ingredient and step]

                Narrator: "replace this with How to do this step of cooking with details"
                '''
            },
            {
                'role':'system',
                'content': f''' below is a good example of what you should generate, of course changing it to fit {source_material}:


1)  [Background image: all the ingredients on a table from {source_material}]

Narrator: "Here are all the ingredients you'll need: 1 pound ground beef, 2 cups rice, 3 onions , a clove of garlic, and 2 tablespoons of paprika "

2) [Background image: Bowl of mixed ground beef, rice, onion, garlic, and spices]

Narrator: "Combine ground beef, rice, onion, garlic, spices to make the stuffing mixture for the cabbage rolls."

3) [Background image: Cabbage leaf being filled with the beef mixture]

Narrator: "Carefully fill cabbage leaves with the beef mixture, then roll them up ensuring the sides are tucked in."

4) [Background image: Cabbage rolls placed in a pot with tomato sauce and diced tomatoes]

Narrator: "Place cabbage rolls in a pot, pour over tomato sauce, diced tomatoes, season, then cover and simmer for 45-60 minutes."

5) [Background image: Delicious stuffed cabbage rolls ready to be served]

Narrator: "After simmering, serve hot, and enjoy your delectable stuffed cabbage rolls!"
                '''
            },
            {
                'role': 'user',
                'content': f'create a Youtube Short narration based on the following source material, emphasizing the exact steps of the recipe, and the first narration should be the needed ingredients: \n\n {source_material}'
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

    img_path = f"{name}/images"
    # imgs_paths = sorted(os.listdir(img_path))
    fps = 30 
    mp4 = f'cooking_with_captions_{name}.mp4'
    output_dir = f'{name}'

    video.images_to_video(img_path, 'video_no_sound.avi', 'video.mp4', data_json, output_dir, name, fps=30)

    return name

