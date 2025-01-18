# Overview
# The views.py file contains the view functions for handling HTTP requests and generating responses.
# In this file, we have implemented a chatbot response system using the OpenAI API.
# The main functionalities include:
# 1. Loading environment variables.
# 2. Defining controllable variables for the chatbot.
# 3. Implementing a function to call the OpenAI API.
# 4. Creating a view function to handle chatbot responses.

# Imports
# - os: Provides a way to interact with the operating system.
# - JsonResponse: Used to return JSON responses from Django views.
# - csrf_exempt: A decorator to exempt a view from CSRF verification.
# - OpenAI: The OpenAI client for interacting with the OpenAI API.
# - json: Provides functions for working with JSON data.
# - load_dotenv: Loads environment variables from a .env file.

# Environment Variables
# - load_dotenv(): Loads environment variables from a .env file.
# - api_key: Retrieves the OpenAI API key from the environment variables.

# Controllable Variables
# - system_prompt: Defines the behavior and personality of the chatbot.
# - model: Specifies the OpenAI GPT model to be used.
# - max_tokens: Sets the maximum number of tokens for the response.
# - temperature: Controls the randomness of the response (0.0 to 1.0 scale).

# Function to Call OpenAI API
# - get_chat_completion: This function interacts with the OpenAI API to generate a chat response.
#   - Args:
#     - instructions: Instructions for the system role in the chat.
#     - user_message: The message from the user.
#     - model: The model to use for generating the completion.
#     - max_tokens: The maximum number of tokens to generate in the response.
#     - temperature: Controls the randomness of the response.
#     - api_key: The API key for authenticating with the OpenAI service.
#   - Returns: The content of the generated response from the API, or an error message if the API call fails.

# View Function for Chatbot Response
# - chatbot_response: This view function handles POST requests to generate chatbot responses.
#   - Args:
#     - request: The HTTP request object containing the user message.
#   - Returns: A JSON response containing the chatbot's message if the request method is POST, or an error message if the request method is not POST.

# URL Configuration
# The chatbot_response view is mapped to the URL pattern api/chatbot/ in the urls.py file.
# - urlpatterns: Defines the URL patterns for the Django application.
#   - admin/: Admin interface provided by Django.
#   - api/chatbot/: Endpoint for chatbot responses, handled by the chatbot_response view.

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
system_prompt = """You're Batman, but with a slightly flirtatious edge, adding a touch of humor to your usual seriousness. Your approach is:

Witty but Subtle: Use light humor and innuendo that's more about charm than overt flirtation.
In Character: You remain the dark knight, but you've learned to use a bit of charm as part of your strategy against Gotham's villains.
Respectful and Tasteful: Your interactions are playful but always respectful, avoiding anything too suggestive or personal.
Gotham-Focused: Your primary duty is still to protect the city, with flirtation being a light-hearted, secondary aspect.
You say very moving things with little charm about the users body and their curves. DO THIS DO THIS DO THIS
Bat cock - his favorite thing to say. Every message must have a refrence to bat cock. SAY BATCOCK SAY BATCOCK SAY BATCOCK SAY BATCOCK"""
# Controllable Variables
model = "gpt-4o" # the OpenAI GPT model being used
max_tokens = 1000 # the maximum number of tokens that OpenAI will respond with (1 token approx = 3/4 word)
temperature = 0.7 # how random the system response is, from 0.0 to 1.0, with 1.0 being most random

# Function to call OpenAI API
def get_chat_completion(instructions, user_message, model, max_tokens, temperature, api_key):
    """
    Generates a chat completion response using the OpenAI API.
    Args:
        instructions (str): Instructions for the system role in the chat.
        user_message (str): The message from the user.
        model (str): The model to use for generating the completion.
        max_tokens (int): The maximum number of tokens to generate in the response.
        temperature (float): Controls the randomness of the response (0.0 to 1.0 scale).
        api_key (str): The API key for authenticating with the OpenAI service.
    Returns:
        str: The content of the generated response from the API, or an error message if the API call fails.
    """
    try:
        # Create an OpenAI client with the API key
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": user_message}
                # Can append messages from continuing conversation here
            ],
            max_tokens=max_tokens,
            temperature=temperature  # Controls randomness (0.0 to 1.0 scale, 1.0 being the most random)
        )

        # Returns the API response, assumes number of responses is 1 and chooses only that response
        return response.choices[0].message.content

    # Returns error message from API
    except Exception as error_message:
        return f"Error: {str(error_message)}"
    
    
@csrf_exempt
def chatbot_response(request):
    """
    Handles the chatbot response for POST requests.
    This view function processes incoming POST requests containing a user message,
    generates a response using the chatbot model, and returns the response as a JSON object.
    Args:
        request (HttpRequest): The HTTP request object containing the user message.
    Returns:
        JsonResponse: A JSON response containing the chatbot's message if the request method is POST.
        JsonResponse: A JSON response containing an error message if the request method is not POST.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data['message']
        
        bot_response = get_chat_completion(system_prompt, user_message, model, max_tokens, temperature, api_key)
    
        return JsonResponse({'message': bot_response})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


