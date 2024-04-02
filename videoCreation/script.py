from openai import OpenAI
import os
from dotenv import load_dotenv
import narration
import json
import images
import video


load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")

narration_api = 'openai' # 'elevenlabs' 


# print('about to task for input')
# user_input = input("what would you like to eat?: ")
# print('received input')
def run(prompt):
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
    
    # with open('data.json', 'r') as f:
    #     data_json = json.load(f)

    # img_path = f"/Users/tylerklimas/Desktop/openaisandbox/videoCreation/images/{name}"
    # # imgs_paths = sorted(os.listdir(img_path))
    # fps = 30 
    # mp4 = f'{name}.mp4'

    # video.images_to_video(img_path, f'cooking_with_captions_{name}.mp4', mp4, data_json, fps)

    response_1 =  client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    'role':'system',
                    'content': ''' Your job is to give recipe with clear and straigtforward steps. 
                    Skip the thematic answers and give numbered steps of about 2 sentances each. Before the steps, give a list all the needed ingredients and quantities.
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
                'content': '''You are a youtube short recipe narration generator, 
                emphasize the steps and not thematic presentation, 
                30 seconds to 1 minute narration,
                the narration you create will have a picture background for each step.
                
                respond with the following format with however many steps of the recipe:

                1) [Background image: Description of image first Ingredient and step]

                Narrator: "A few sentences of the cooking step details"

                2) [Background image: Description of image second Ingredient and step]

                Narrator: "How to do this step of cooking with details"

                ... continue for all the steps
                '''
            },
            {
                'role': 'user',
                'content': f'create a Youtube Short narration based on the following source material, emphasizing the exact steps of the recipe: \n\n {source_material}'
            }
        ]

    )
    response = response.choices[0].message.content

    data = narration.parse(response)
    narration.create(data, name, 'narration')

    os.path.join(name, 'data.json')
    
    with open(os.path.join(name, 'response.txt'), 'w') as f:
        f.write(response)

    with open(os.path.join(name, 'data.json'), 'w') as f:
        json.dump(data, f)

    with open(os.path.join(name, 'data.json'), 'r') as f:
        data_json = json.load(f)


    os.path.join(name, 'images')
    if not os.path.exists(os.path.join(name, 'images')):
        os.makedirs(os.path.join(name, 'images'))

    images.create_from_data(data, name)

    img_path = f"/Users/tylerklimas/Desktop/openaisandbox/videoCreation/{name}images"
    # imgs_paths = sorted(os.listdir(img_path))
    fps = 30 
    mp4 = f'cooking_with_captions_{name}.mp4'

    video.images_to_video(img_path, 'cooking_with_captions_chinese.mp4', mp4, data_json, fps)


