import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()
# API Key
api_key = os.getenv('OPENAI_API_KEY')

# Inputs
instructions = "You answer riddles in unconventional ways, and you think and talk like Batman" # how the system behaves, like who it is
prompt = "What would happen if Peter Piper picked a patch of pickled peppers?" # what the system is responding to, like what a person hears and responds to in conversation

# Controllable Variables
model = "gpt-3.5-turbo" # the OpenAI GPT model being used
max_tokens = 1000 # the maximum number of tokens that OpenAI will respond with (1 token approx = 3/4 word)
temperature = 0.7 # how random the system response is, from 0.0 to 1.0, with 1.0 being most random



# Function to call OpenAI API
def get_chat_completion(instructions, user_message, model, max_tokens, temperature, api_key):
    try:
        # Create an OpenAI cleint with the API key
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": user_message}
            ],
            max_tokens=max_tokens,
            temperature=temperature  # Controls randomness (0.0 to 1.0 scale, 1.0 being the most random)
        )

        # Returns the API response, assumes number of responses is 1 and chooses only that response
        return response.choices[0].message.content

    # Returns error meessage from API
    except Exception as error_message:
        return f"Error: {str(error_message)}"
    
    
@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data['message']
        

        bot_response = get_chat_completion(instructions, user_message, model, max_tokens, temperature, api_key)
    
        return JsonResponse({'message': bot_response})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)