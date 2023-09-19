import openai
import random

# I would like to control the amount of prompts I can make and seed them with random numbers



# Set your OpenAI API key here
api_key = "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"
openai.api_key = api_key

def generate_prompt(seed):
    return f"""
Name of Band: 
Name of Song: 
Trivia: 
{seed}"""

def generate_system_prompt():
    return """You are to generate a name and information for a new Jazz band that never existed at each iteration. 
    You will fill each field with the relevant information and keep the format of the form, this template to fill in include name of band, name of song, and trivia fact. Below are 7 correct examples of the template and 4 incorrect examples
     
     #1 Correct Template
     Name of Band: The Three Toothed Pretenders
     Name of Song: I Have too Much Love Baby
     Trivia: When founding the band, band leader Terry Grupo gambled his last two hundred dollars in a New Orleans casino to win the money to buy instruments for the band.
       
     #2 Correct Template
     Name of Band: Summer Girls
     Name of Song: Wonder Years
     Trivia: After a long dispute between bandmates Terresa Wonder and Sally True, the band resolved never to play this song again.
       
     #3 Correct Template
     Name of Band: Street Fishes
     Name of Song: They Only Say Goodbye if They Mean it
     Trivia: Drummer Sal Garcia was arrested and sentenced to twenty years for armed robbery in 1963.
       
     #4 Correct Template
     Name of Band: The Jimmy Brand Band
     Name of Song: Last Nights
     Trivia: Originally a bonus song that the band routinely played to warm up. It became a US Charts top 5 hit in 1972.
        
     #5 Correct Template
     Name of Band: Nelly Langford
     Name of Song: Love You till the Sun Go Down
     Trivia: Nelly Langford grew up the daughter of a Baptist Minister in Montgomery Alabama 
    
     #6 Correct Template
     Name of Band: The New Marks 
     Name of Song: Running Smooth
     Trivia: The New Marks disbanded in 1958 after Saxophonist Willard Pill became a tax accountant.
    
     #7 Correct Template
     Name of Band: New Orleans Star Band
     Name of Song: We are the Rhythm
     Trivia: This song became a hit for the band after being featured in the hit movie of 1954 'Center Stage'.
     
     INCORRECT EXAMPLES BELOW 

     #1 Incorrect
     Name of Band: 1945uf
     Name of Song: Name of Song
     Trivia: Trivia is defined as etc.

     (This is incorrect because: Numbers where there should be words, restating of prompt, definition or example of unrelated trivia.)
       
     #2 Incorrect
     Name of Band: name of band
     th Song: name of song
     Trivia: Jazz is a music genre that was founded in the United States.

     (This is incorrect because: restating of prompt, editing the 'Name of the Song' field, and unrelated trivia to the band)
       
     #3 Incorrect
     Name of Band: The Rolling Stones
     Name of Song: Sympathy for the Devil
     Trivia: The concept for 'Sympathy for the Devil' is inspired by the Russian Novel 'The Master and Margarita' .

     (This is incorrect because: This is information of a real band that existed. You must never use historical information)

     #4 Incorrect 
     .
     th:
     The band was formed in 1968 in Brooklyn, when Sally Sue Molten approached Jessie Snow in the One Eyed Cat bar

     (This is incorrect because the formatting of the queries namely 'Name of Band' and and 'Name of Song' have been modified)
                     
                                     """


if __name__ == "__main__":
    num_prompts = 3  # Number of prompts to generate
    for i in range(num_prompts):
        seed = random.randint(1, 1000)  # Generate a random seed
        prompt = generate_prompt(seed)
        system_prompt = generate_system_prompt()
        combined_prompt = f"{system_prompt}\n\n{prompt}"
        
        # Make an API call to ChatGPT
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can use any engine here
            prompt=combined_prompt,
            max_tokens=100  # Adjust the number of tokens as needed
        )
        
        # Print the generated response
        generated_response = response.choices[0].text.strip()
        print(f"Generated Response {i + 1}:\n\n{generated_response}\n{'=' * 40}")

        
        
        # Save the prompts and responses to separate files
        with open(f"prompt_{i + 1}.txt", "w") as prompt_file:
            prompt_file.write(combined_prompt)
        
        with open(f"response_{i + 1}.txt", "w") as response_file:
            response_file.write(generated_response)

#def djscript(reponse):
    
    









