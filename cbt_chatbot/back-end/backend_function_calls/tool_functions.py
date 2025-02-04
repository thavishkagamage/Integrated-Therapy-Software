# All function defenitions that correspond with tools in the tools.py file

# Functions should hve the same name as the tool it corresponds to:
#   This allows us to call a function defined here based on the name of the tool passed in by the API response

import json

def detect_self_harm(**kwargs):
    user_response = kwargs.get('user_response', 'No user response provided')
    return f"You said '{user_response}', which indicates you may harm yourself or harm others. Please call 911 or go to your nearest emergency room."

def start_cbt(**kwargs):
    return "You said something that indicates you want to begin a CBT session"

# Dictionary to map the function name from the response to the function it corresponds to
function_mapping = {
    "detect_self_harm": detect_self_harm,
    "start_cbt": start_cbt
}

# Handle the function call from OpenAI API response
def handle_response(message):
    """
    Extracts the function name and arguments from the OpenAI API response message, and calls the corresponding function with the argments
    Args:
        message: The message from the OpenAI API response containing the function call.
    Returns:
        The result of the function call.
    """
    try:
        # Extract function name and arguments from the message in the API response
        function_name = message.tool_calls[0].function.name
        function_args = json.loads(message.tool_calls[0].function.arguments)
        print('\n' + str(function_name) + ' : ' + str(function_args) + '\n') # debug line

        # Check if function exists in function_mapping
        if function_name in function_mapping:
            result = function_mapping[function_name](**function_args) # call the function with the arguments
        else:
            # TODO Need to handle case where function name is not in the mapping and keep conversation going
            return f"Error: Function '{function_name}' not recognized."
        return result

    except Exception as error_message:
        return f"Error: {str(error_message)}"