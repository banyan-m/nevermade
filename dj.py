from elevenlabs import generate, play, set_api_key,Voice, VoiceDesign, Gender, Age, Accent
import os
import openai
import random



set_api_key("cae4c753ad710c7d68433594a8134e50")

api_key_openai = "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"
openai.api_key = api_key_openai


def generate_prompt(seed):
    return f"""{seed} You are an old Lousiana man from the bayou, youve been listening to Jazz since before Louis Armstrong 
            and have a weary old worn voice from a tough life fully lived, like that of an old southermn trumpet that has smoked many cigarettes
            and drank many bottles of whiskey. From the recieved information template recieved in this message which
            includes a name of a band, a name of a song, and a trivia fact about the band, you will generate a radio station style aside
            relating to your life and the band, perhaps you went to concert or met the band, perhaps once you broke up with your girlfriend and 
            this song played on the radio as it poured rain in the bayou. Whatever the case, you often say relate information to a a story an old friend named Joe once told you
            and you often are relating the songs to your hard lived life of odd jobs and failed relationships """

if __name__ == "__main__":
    num_prompts = 3  # Number of prompts to generate

    for i in range(num_prompts):
       
        
        prompt_path = os.path.join(os.path.dirname(__file__), f"response_{i + 1}.txt")
        with open(prompt_path, "r") as f:
            generated_prompt = f.read()
        
        
        seed = random.randint(1, 1000)  # Generate a random seed
        system_prompt = generate_prompt(seed)

        # Make an API call to ChatGPT using 3.5 model with added system prompt
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": generated_prompt}
            ],
            temperature=1,
            max_tokens=256 
        )

        generated_response = response['choices'][0]['message']['content']

        # Print the generated response
        print(f"Generated Response {i + 1}:\n\n{generated_response}\n{'=' * 40}")




        