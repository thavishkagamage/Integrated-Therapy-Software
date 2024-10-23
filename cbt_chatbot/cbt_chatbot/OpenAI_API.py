'''
Owner: Alex Gribble
Last Edit: AGG 10/21/24

Description: Uses OpenAI API to generate text from prompt
Libraries: OpenAI
'''

from openai import OpenAI
client = OpenAI()

# Inputs
instructions = "You answer riddles in unconventional ways, and you think and talk like Batman" # how the system behaves, like who it is
prompt = "What would happen if Peter Piper picked a patch of pickled peppers?" # what the system is responding to, like what a person hears and responds to in conversation

# Controllable Variables
model = "gpt-3.5-turbo" # the OpenAI GPT model being used
max_tokens = 1000 # the maximum number of tokens that OpenAI will respond with (1 token approx = 3/4 word)
temperature = 0.7 # how random the system response is, from 0.0 to 1.0, with 1.0 being most random

# OpenAI API key (create env variable for this)
api_key = 'it was here'

# Function to call OpenAI API
def get_chat_completion(instructions, prompt, model, max_tokens, temperature, api_key):
    try:
        # Create an OpenAI cleint with the API key
        client = OpenAI.api_key(api_key)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature  # Controls randomness (0.0 to 1.0 scale, 1.0 being the most random)
        )

        # Returns the API response, assumes number of responses is 1 and chooses only that response
        return response['choices'][0]['message']['content'].strip()

    # Returns error meessage from API
    except Exception as error_message:
        return f"Error: {str(error_message)}"

# Print API message
print(get_chat_completion(instructions, prompt, model, max_tokens, temperature))
