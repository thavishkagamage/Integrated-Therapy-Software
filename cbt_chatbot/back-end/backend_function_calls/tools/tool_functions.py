# All function defenitions that correspond with tools in the tools.py file

import json
# from django.http import JsonResponse
# from conversation_handler.models import Conversation
from backend_function_calls.session_utils import get_conversation_object

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

CONVERSATION_ID = -1
AGENDA_DICT = {}

def detect_self_harm(**kwargs):
    user_response = kwargs.get('user_response', 'No user response provided')
    conversation = get_conversation_object(CONVERSATION_ID)

    try: # Turn on crisis mode
        conversation.isCrisisModeActive = True
        conversation.save(update_fields=['isCrisisModeActive'])
        print(f"{YELLOW}CRISIS MODE ACTIVE{RESET}.\n")
    except Exception as error:
        print(f'{RED}ERROR:{RESET} {error}\n')

    return f"The user said '{user_response}', which indicates they may harm themselves or harm others. Tell them to call 911 or go to your nearest emergency room, then provide emotional support."

def current_agenda_item_is_complete():
    # get the conversation
    conversation = get_conversation_object(CONVERSATION_ID)
    
    # fetch agenda from conversation object
    updated_agenda_statuses = conversation.current_sub_items

    # mark current agenda item as complete
    for index, item in enumerate(updated_agenda_statuses):
        if item == 1:
            updated_agenda_statuses[index] = 2
            print(f"{GREEN}AGENDA UPDATE:{RESET} item marked complete at {index=}\n")
            break

    # update and save agenda statuses in the conversation object
    try:
        conversation.current_sub_items = updated_agenda_statuses
        conversation.save(update_fields=['current_sub_items'])
    except Exception as error:
        print(f'{RED}ERROR:{RESET} {error}\n')

    return updated_agenda_statuses

def pick_new_current_agenda_item(**kwargs):
    print(f"{GREEN}AGENDA UPDATE:{RESET} new current agenda item is: " + str(kwargs.get('agenda_item_index', 'ERR')) + ": " + str(kwargs.get('agenda_item', 'ERR')))
    
    # get the conversation
    conversation = get_conversation_object(CONVERSATION_ID)
    
    # fetch agenda from conversation object
    updated_agenda_statuses = conversation.agenda_items
    print(f"{GREEN}AGENDA UPDATE:{RESET} updated agenda statuses: " + str(updated_agenda_statuses) + "\n")

    new_agenda_item = kwargs.get('agenda_item', '')
    new_agenda_item_index = kwargs.get('agenda_item_index', -1)

    # SAFETY MEASURE
    # Check if the new agenda item is valid and not already completed
    agenda_dict_keys = [key.lower() for key in AGENDA_DICT.keys()] # convert keys to lowercase for case insensitive comparison
    if (new_agenda_item.lower() not in agenda_dict_keys) or (new_agenda_item_index == -1) or (updated_agenda_statuses[new_agenda_item_index] != 0):
        # get index of first not started item
        new_agenda_item_index = updated_agenda_statuses.index(0)
        print(f"{YELLOW}AGENDA UPDATE SAFETY MEASURE:{RESET} Invalid new agenda item or already completed. Defaulting to first not started agenda item at index {new_agenda_item_index}.\n")

    # update and save agenda statuses in the conversation object
    try:
        # use agenda_item_index to assign the new agenda item as current
        updated_agenda_statuses[new_agenda_item_index] = 1
        conversation.agenda_items = updated_agenda_statuses
        conversation.save(update_fields=['agenda_items'])
    except Exception as error:
        print(f'{RED}ERROR:{RESET} {error}\n')

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
def handle_response(message, conversation_id, agenda_dict):
    """
    Extracts the function name and arguments from the OpenAI API response message, and calls the corresponding function with the argments
    Args:
        message: The message from the OpenAI API response containing the function call.
    Returns:
        The result of the function call.
    """   

    global CONVERSATION_ID
    CONVERSATION_ID = conversation_id
    global AGENDA_DICT
    AGENDA_DICT = agenda_dict

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
        return f"{RED}Error:{RESET} {str(error_message)}"