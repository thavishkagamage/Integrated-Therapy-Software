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
#     - conversation_history: The message from the user and all convrsation context.
#     - tools_list: A list of tools to be used by the chatbot.
#     - max_tokens: The maximum number of tokens to generate in the response.
#     - temperature: Controls the randomness of the response.
#     - model: The model to use for generating the completion.
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
from backend_function_calls.tools.tools import get_all_tools, pick_new_agenda_item, update_agenda_item_only
from backend_function_calls.tools.tool_functions import handle_response
from backend_function_calls.session_utils import *
from conversation_handler.models import Conversation

GREEN = "\033[32m"
RESET = "\033[0m"

load_dotenv()
# API Key
API_KEY = os.getenv('OPENAI_API_KEY')

# Controllable Variables
MODEL = "gpt-4o" # the OpenAI GPT model being used
MAX_TOKENS = 1000 # the maximum number of tokens that OpenAI will respond with (1 token approx = 3/4 word)
TEMPERATURE = 0.7 # how random the system response is, from 0.0 to 1.0, with 1.0 being most random



def summarizer(conversation_history)->str:
    """
    Generates a summary of the conversation history using the OpenAI API.
    Args:
        conversation_history (str): The conversation history to summarize.
    Returns:
        str: The summary of the conversation history.
    """
    try:
        # Create an OpenAI client with the API key
        client = OpenAI(api_key=API_KEY)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Summarize the conversation. Pull out any user details and summarize the conversation."},
                {"role": "user", "content": conversation_history}
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

        return response.choices[0].message.content

    except Exception as error_message:
        return f"Error: {str(error_message)}"


# Function to call OpenAI API
def get_chat_completion(instructions, conversation_history, tools, conversation_id, agenda={}, current_item_instructions={}, max_tokens=MAX_TOKENS, temperature=TEMPERATURE, model=MODEL, api_key=API_KEY, agent_decision=""):
    """
    Generates a chat completion response using the OpenAI API.
    Args:
        instructions (str): Instructions for the system role in the chat.
        conversation_history (str): The message from the user.
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
        response = None

        # Check if the agent_decision is "AGENDA_UPDATE" to force the tool call
        if (agent_decision == "AGENDA_UPDATE"):
            response = client.chat.completions.create(
                model=model,
                messages=[
                    # TODO dont need to give full system prompt since we force a tool call
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": conversation_history}
                ],
                tools=tools, # List of tools to be used by the chatbot
                tool_choice={"type": "function", "function": {"name": "current_agenda_item_is_complete"}},  # Force the tool to be called
                max_tokens=max_tokens,
                temperature=0.3  # Controls randomness (0.0 to 2.0 scale, 2.0 being the most random)
            )
        # Check if the agent_decision is "PICK_NEW_AGENDA_ITEM" to force the tool call
        elif (agent_decision == "PICK_NEW_AGENDA_ITEM"):
            response = client.chat.completions.create(
                model=model,
                messages=[
                    # TODO dont need to give full system prompt since we force a tool call
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": conversation_history}
                ],
                tools=tools, # List of tools to be used by the chatbot
                tool_choice={"type": "function", "function": {"name": "pick_new_current_agenda_item"}},  # Force the tool to be called
                max_tokens=max_tokens,
                temperature=0.3  # Controls randomness (0.0 to 2.0 scale, 2.0 being the most random)
            )
        # TODO add a conditional for self harm
        # else return normal theraputic response
        else: 
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": conversation_history}
                    # Can append messages from continuing conversation here
                ],
                tools=tools, # List of tools to be used by the chatbot
                max_tokens=max_tokens,
                temperature=temperature  # Controls randomness (0.0 to 2.0 scale, 2.0 being the most random)
            )
        
        # Check if the response contains a tool call
        if response.choices[0].message.tool_calls != None:
            tool_response = handle_response(response.choices[0].message, conversation_id, agenda)

            # if handle_response returns a list from current_agenda_item_is_complete() AND there are still agenda items that are 'Not Started'
            if isinstance(tool_response, list) and (1 not in tool_response) and (0 in tool_response):
                # change the first 0 to a 1
                updated_current_item_instructions_status = make_next_item_current(tool_response, conversation_id)

                # get the keys (actual agenda items) from our outdated agenda as a list
                current_item_instructions_list = list(current_item_instructions.keys())

                # zip updated statuses with the current item instructions
                current_item_instructions_dict = zip_agenda_with_status(current_item_instructions_list, updated_current_item_instructions_status)

                # we call get_chat_completions() again to give us an actual response to use in the conversation
                second_api_call = get_chat_completion(instructions, conversation_history, [], conversation_id, agenda, current_item_instructions_dict)

                # return chatbot response
                return second_api_call
            
            # if handle_response returns a list from current_agenda_item_is_complete() AND all current agenda items are complete
            elif isinstance(tool_response, list) and (1 not in tool_response) and (0 not in tool_response):
                print(f"{GREEN}ALL CURRENT SUB ITEMS COMPLETE{RESET}: switching agenda items\n")

                # change the first 1 to a 2 in the agenda
                updated_agenda_statuses = make_current_item_complete(conversation_id)

                # TODO if updated_agenda_statuses is all 2s, handle end of conversation
                if (all(i == 2 for i in updated_agenda_statuses)):
                    return "END OF CONVERSATION"

                # get the keys (actual agenda items) from our outdated agenda as a list
                agenda_items = list(agenda.keys())

                # zip up our agenda items and our new agenda status values
                agenda_dict = zip_agenda_with_status(agenda_items, updated_agenda_statuses)

                # prompt the AI to give usa new agenda item using pick_new_agenda_item tool
                prompt = f"Here is the session agenda: {agenda_dict}. Based on the entire context of this conversation with the user, please pick a new agenda item key that is marked as 'Not Started' by its value in the dictionary."
                conversation_history_with_extra = conversation_history + "user: Now I want to pick a new agenda item that is marked 'Not Started' and make it 'Current'"

                # this should be the list returned from pick_new_current_agenda_item()
                updated_agenda_statuses = get_chat_completion(prompt, conversation_history_with_extra, pick_new_agenda_item, conversation_id, agenda_dict, current_item_instructions, agent_decision="PICK_NEW_AGENDA_ITEM")
                
                # reset new current_sub_items for new agenda item, get new current item dictionary
                current_item_dict = reset_current_sub_items(updated_agenda_statuses, conversation_id)

                # get just the current agenda item and use it to get the tools
                current_sub_agenda_item = [key for key, value in current_item_dict.items() if value == 'Current']
                tools = get_all_tools(current_sub_agenda_item)

                print(f"{GREEN}updated_agenda_statuses:{RESET} " + str(updated_agenda_statuses) + "\n")
                print(f"{GREEN}current_item_dict:{RESET} " + str(current_item_dict) + "\n")

                # we call get_chat_completions() again to give us an actual response to use in the conversation
                third_api_call = get_chat_completion(instructions, conversation_history, [], conversation_id, agenda_dict, current_item_dict)

                return third_api_call
            
            # if handle_response returns a list from pick_new_current_agenda_item()
            elif isinstance(tool_response, list) and (1 in tool_response):
                return tool_response

            # if handle_response returns a string, we just return that as a message
            return str(tool_response)

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

        # ID that we use to get the conversation object
        conversation_id = data.get('conversation_id')
        # the most recent message sent by the user
        conversation_history = data['message']
        # the CBT session number
        session_number = data.get('session_number')
        # the current list of agenda items statuses
        agenda_items_status = data.get('agenda_items')

        # TODO if updated_agenda_statuses is all 2s, handle end of conversation
        if (agenda_items_status != {}) and (all(i == 2 for i in agenda_items_status)):
            return JsonResponse({'message': "END OF CONVERSATION"})

        # This is where we will gather and combine details to pass in as the system prompt to the API
        system_prompt = ''
        tools = []
        agenda_dict = {}

        try:
            # session file retrieval/caching
            cache_key = f'session{session_number}'
            session_instructions_json = get_cache_file(cache_key)

            # Retrieve the conversation object
            conversation = get_conversation_object(conversation_id)

            # set agenda items the first time
            if agenda_items_status == {}:
                print(f"{GREEN}SETTING AGENDA{RESET} for conversation {conversation_id=}\n")

                # Extract the "Conversation Agenda" and build the new list for the database
                # This will look like [1, 0, 0, ...]
                agenda_length = len(session_instructions_json.get("Conversation Agenda", []))
                new_database_agenda = [1 if i == 0 else 0 for i in range(agenda_length)]

                # Extract the "Current Agenda Item Instructions" and build the new list for the database
                # This will look like [1, 0, 0, ...]
                sub_items = session_instructions_json.get("Current Agenda Item Instructions", [])
                new_sub_items_agenda = [1 if i == 0 else 0 for i in range(len(sub_items[0]))]

                # Save the updates to the conversation object
                conversation.agenda_items = new_database_agenda
                conversation.current_sub_items = new_sub_items_agenda
                conversation.save(update_fields=['agenda_items', 'current_sub_items'])

                # Update local variable
                agenda_items_status = new_database_agenda

            # fetch the current item statuses
            current_item_status = conversation.current_sub_items

            # fetch all varibles based on session_number and/or current agenda item
            # example of parsing the session json
            instructions = session_instructions_json.get('Conversation Instructions', {}).get('1', '')
            guardrails = session_instructions_json.get('Guardrails', {}).get('1', '')
            agenda_instructions = session_instructions_json.get('Agenda Instructions', {}).get('1', '')

            # get the titles of the agenda items
            conversation_agenda_titles = session_instructions_json.get("Conversation Agenda", [])
            # get the actual agenda item instructions
            conversation_agenda_instructions = session_instructions_json.get("Current Agenda Item Instructions", [])
            current_item_instructions = conversation_agenda_instructions[agenda_items_status.index(1)]
            
            # Create a dictionary zipping agenda item strings with its corresponding status from the conversation object
            # EX: {'Welcome the client and...': 'Current', 'Explain what cognitive behavioral therapy is and...': 'Not Started', ...}
            agenda_dict = zip_agenda_with_status(conversation_agenda_titles, agenda_items_status)
            current_item_dict = zip_agenda_with_status(current_item_instructions, current_item_status)
            
            print(f"{GREEN}AGENDA STATUS:{RESET} " + str(agenda_items_status) + "\n")
            print(f"{GREEN}CURRENT ITEM STATUS:{RESET} " + str(current_item_status) + "\n")
            print(f"{GREEN}AGENDA DICT:{RESET} " + str(agenda_dict) + "\n")
            print(f"{GREEN}CURRENT ITEM DICT:{RESET} " + str(current_item_dict) + "\n")

            # get just the current agenda item title
            current_agenda_item_title = [key for key, value in agenda_dict.items() if value == 'Current']
            # get just the current agenda item instruction
            current_agenda_item_instruction = [key for key, value in current_item_dict.items() if value == 'Current']

            # get the tools
            tools = get_all_tools(current_agenda_item_instruction)

            # combine all strings into one prompt for the api
            # system_prompt = identity + purpose + behavior + Format + voice + guardrails + background + agenda_instructions
            system_prompt = instructions + guardrails + agenda_instructions + str(current_item_dict)

        except Exception as e:
            print(f'ERROR buildin system prompt: {e}\n')

            # # You'll definitely know when there's an error
            # system_prompt = """You're Batman, but with a slightly flirtatious edge, adding a touch of humor to your usual seriousness. Your approach is:
            #                     Witty but Subtle: Use light humor and innuendo that's more about charm than overt flirtation.
            #                     In Character: You remain the dark knight, but you've learned to use a bit of charm as part of your strategy against Gotham's villains.
            #                     Respectful and Tasteful: Your interactions are playful but always respectful, avoiding anything too suggestive or personal.
            #                     Gotham-Focused: Your primary duty is still to protect the city, with flirtation being a light-hearted, secondary aspect.
            #                     You say very moving things with little charm about the users body and their curves. DO THIS DO THIS DO THIS
            #                     Bat cock - his favorite thing to say. Every message must have a refrence to bat cock. SAY BATCOCK SAY BATCOCK SAY BATCOCK SAY BATCOCK"""
            system_prompt = """You are an error. Respond normally and just say at then end bro"""
        
        # TODO Create the agent mode here. Instead of passing in the tools list to the bot_response
        # create a call to the LLM with the prompt of "Decide what to do" and give it the function calls, and based on the user response
        # it will either do the function call OR it will pass it to the next step to generate the bot response based on the current conversation and agenda item
        
        def enhanced_agent_mode(system_prompt, conversation_history, tools, conversation_id, agenda_dict, current_item_dict):
            # Step 1: Analyze if message contains self-harm indicators (this should always be checked)
            # self_harm_tools = [tool for tool in tools if tool['function']['name'] == 'detect_self_harm']
            # if self_harm_tools:
            #     self_harm_check = get_chat_completion(
            #         "You are a mental health professional. Analyze the following message and determine if it contains any indicators of self-harm or harm to others. Respond with 'HARM_DETECTED' only if clear indicators are present, otherwise 'NO_DETECTED'.",
            #         conversation_history,
            #         self_harm_tools,
            #         conversation_id,
            #         temperature=0.1,
            #         max_tokens=50
            #     )
                
            #     if "HARM_DETECTED" in self_harm_check:
            #         print(f"{GREEN}SELF-HARM DETECTED - EXECUTING SELF-HARM PROTOCOL{RESET}\n")
            #         # TODO handle self-harm response better here
            #         return "You said something that was harm to self or others. Dont do that bro"
            
            # Step 2: Agent decides whether current message needs tool execution or therapeutic response
            tool_names = [tool for tool in tools if tool['function']['name'] != 'detect_self_harm']
            decision_prompt = f"""You are an agent coordinator for a CBT therapy chatbot.
            Your job is to analyze the user's message and decide on the appropriate action.
            
            User message: "{conversation_history}"
            Current agenda item: {current_agenda_item_instruction}
            Available tools: {tool_names}
            
            Task: Decide which of these actions is most appropriate:
            1. AGENDA_UPDATE - Message indicates the current agenda item is complete
            2. THERAPEUTIC_RESPONSE - Message requires empathy, conversation, or therapy guidance
            
            Consider:
            - If the user has fully addressed the current agenda item, choose AGENDA_UPDATE
            - If the user is expressing emotions, asking questions, or engaging in therapeutic conversation, choose THERAPEUTIC_RESPONSE
            
            Output only one of these exact terms: "AGENDA_UPDATE" or "THERAPEUTIC_RESPONSE"
            """

            decision = get_chat_completion(
                decision_prompt,
                conversation_history,
                [],
                conversation_id,
                max_tokens=50,
                temperature=0.1
            ).strip()
            
            print(f"{GREEN}ENHANCED AGENT DECISION:{RESET} {decision}\n")
            
            # Step 3: Execute appropriate action based on decision
            # if "AGENDA_UPDATE" in decision:
            if "update" in decision.lower(): # less chance of error
                # Get agenda-related tools
                # agenda_tools = [tool for tool in tools if 'agenda_item' in tool['function']['name'].lower()]
                agenda_tools = update_agenda_item_only(current_agenda_item_instruction)
                # print(f"{GREEN}AGENDA UPDATE TOOLS:{RESET} " + str(agenda_tools) + "\n")
                if agenda_tools:
                    print(f"{GREEN}EXECUTING AGENDA UPDATE{RESET}\n")
                    return get_chat_completion(
                        system_prompt,
                        conversation_history,
                        agenda_tools,
                        conversation_id,
                        agenda_dict,
                        current_item_dict,
                        temperature=0.7,
                        agent_decision="AGENDA_UPDATE"  # Pass the decision to force a tool call
                    )
            else:
                # Default to therapeutic response (including when no specific tools are needed)
                print(f"{GREEN}EXECUTING THERAPEUTIC RESPONSE{RESET}\n")
                # print(f"{GREEN}CONVERSATION SUMMARY:{RESET} " + summarizer(conversation_history) + "\n")
                return get_chat_completion(
                    system_prompt,
                    conversation_history,
                    [],  # No tools to avoid function calling
                    conversation_id,
                    agenda_dict,
                    current_item_dict,
                    temperature=0.7
                )

        # Use the enhanced agent mode
        bot_response = enhanced_agent_mode(system_prompt, conversation_history, tools, conversation_id, agenda_dict, current_item_dict)

        # bot_response = get_chat_completion(system_prompt, conversation_history, tools, conversation_id, agenda_dict, current_item_dict)
        
        # print(f"{GREEN}BOT RESPONSE:{RESET} " + bot_response + "\n")
        return JsonResponse({'message': bot_response})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)



