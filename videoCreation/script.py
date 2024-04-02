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
                    'content': f'create a Youtube Short narration based for the following {user_input}, emphasizing the exact steps of the recipe: '
                }
            ]

        )
    response_recipe = response_1.choices[0].message.content

    with open("recipe.txt", "w") as file:
        file.write(response_recipe)

    with open("recipe.txt") as f:
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
    narration.create(data, 'narration')

    with open('response.txt', 'w') as f:
        f.write(response)

    with open('data.json', 'w') as f:
        json.dump(data, f)

    with open('data.json', 'r') as f:
        data_json = json.load(f)

    if not os.path.exists('images'):
        os.makedirs('images')

    images.create_from_data(data)

    img_path = "/Users/tylerklimas/Desktop/openaisandbox/videoCreation/images"
    # imgs_paths = sorted(os.listdir(img_path))
    fps = 30 
    mp4 = 'cooking_with_captions_chinese_num2.mp4'

    video.images_to_video(img_path, 'cooking_with_captions_chinese.mp4', mp4, data_json, fps)


