# All function defenitions that correspond with tools in the tools.py file

import json
# from django.http import JsonResponse
# from conversation_handler.models import Conversation
from backend_function_calls.session_utils import get_conversation_object

GREEN = "\033[32m"
RESET = "\033[0m"

CONVERSATION_ID = -1

def detect_self_harm(**kwargs):
    user_response = kwargs.get('user_response', 'No user response provided')
    return f"You said '{user_response}', which indicates you may harm yourself or harm others. Please call 911 or go to your nearest emergency room."

def current_agenda_item_is_complete():
    # get the conversation
    conversation = get_conversation_object(CONVERSATION_ID)
    
    # fetch agenda from conversation object
    updated_agenda_statuses = conversation.agenda_items

    # mark current agenda item as complete
    for index, item in enumerate(updated_agenda_statuses):
        if item == 1:
            updated_agenda_statuses[index] = 2
            print(f"{GREEN}AGENDA UPDATE:{RESET} item marked complete at {index=}\n")
            break

    # update and save agenda statuses in the conversation object
    try:
        conversation.agenda_items = updated_agenda_statuses
        conversation.save(update_fields=['agenda_items'])
    except Exception as error:
        print(f'ERROR: {error}\n')

    return updated_agenda_statuses

def pick_new_current_agenda_item(**kwargs):
    print(f"{GREEN}AGENDA UPDATE:{RESET} new current agenda item is: " + str(kwargs.get('agenda_item_index', 'ERR')) + ": " + str(kwargs.get('agenda_item', 'ERR')))
    
    # get the conversation
    conversation = get_conversation_object(CONVERSATION_ID)
    
    # fetch agenda from conversation object
    updated_agenda_statuses = conversation.agenda_items

    # use agenda_item_index to assign the new agenda item as current
    updated_agenda_statuses[kwargs.get('agenda_item_index', -1)] = 1

    # update and save agenda statuses in the conversation object
    try:
        conversation.agenda_items = updated_agenda_statuses
        conversation.save(update_fields=['agenda_items'])
    except Exception as error:
        print(f'ERROR: {error}\n')

    return updated_agenda_statuses

# Dictionary to map the function name from the response to the function it corresponds to
#   - Functions should have the same name as the tool it corresponds to in tools.py
#   - This allows us to call a function defined here based on the name of the tool passed in by the API response
function_mapping = {
    "detect_self_harm": detect_self_harm,
    "current_agenda_item_is_complete": current_agenda_item_is_complete,
    "pick_new_current_agenda_item": pick_new_current_agenda_item
}


# Handle the function call from OpenAI API response
def handle_response(message, conversation_id):
    """
    Extracts the function name and arguments from the OpenAI API response message, and calls the corresponding function with the argments
    Args:
        message: The message from the OpenAI API response containing the function call.
    Returns:
        The result of the function call.
    """   

    global CONVERSATION_ID
    CONVERSATION_ID = conversation_id

    try:
        # Extract function name and arguments from the message in the API response
        function_name = message.tool_calls[0].function.name
        function_args = json.loads(message.tool_calls[0].function.arguments)
        print(f'{GREEN}TOOL TRIGGERED: {RESET}' + str(function_name) + ' : ' + str(function_args) + '\n') # debug line

        # Check if function exists in function_mapping
        if function_name in function_mapping:
            result = function_mapping[function_name](**function_args) # call the function with the arguments
        else:
            # TODO Need to handle case where function name is not in the mapping and keep conversation going
            return f"Error: Function '{function_name}' not recognized."
        return result

    except Exception as error_message:
        return f"Error: {str(error_message)}"