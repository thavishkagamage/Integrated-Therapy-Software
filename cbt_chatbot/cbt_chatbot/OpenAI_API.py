'''
Owner: Alex Gribble
Last Edit: AGG 10/21/24

Description: Uses OpenAI API to generate text from prompt
Libraries: OpenAI
'''

import openai

# Inputs:
instructions = "You answer riddles in unconventional ways, and you think and talk like Batman" # how the system behaves, like who it is
prompt = "What would happen if Peter Piper picked a patch of pickled peppers?" # what the system is responding to, like what a person hears and responds to in conversation

# Controllable Variables:
model = "gpt-3.5-turbo" # the OpenAI GPT model being used
max_tokens = 1000 # the maximum number of tokens that OpenAI will respond with (1 token approx = 3/4 word)
temperature = 0.7 # how random the system response is, from 0.0 to 1.0, with 1.0 being most random

# OpenAI API key (create env variable for this)
openai.api_key = 'your-api-key-here'

# Function to call OpenAI API
def get_openai_response(instructions, prompt, model, max_tokens, temperature):
    try:
        response = openai.Completion.create(
            engine = model,
            prompt = f"{instructions}\n{prompt}", # combines instructions and prompt
            max_tokens = max_tokens,
            n=1,  # Number of responses you want
            stop=None,  # You can specify stopping criteria like "\n" or any custom string
            temperature=0.7  # Controls randomness (0.0 to 1.0 scale, 1.0 being the most random)
        )

        # Extracting and returning the generated text
        return response['choices'][0]['text'].strip() # if n>1, there would be multiple responses to choose from

    except Exception as e:
        return f"Error: {str(e)}"

print(get_openai_response)

# Outputs
# response - what the response of the system was for the instructions and prompt
# e - error response
