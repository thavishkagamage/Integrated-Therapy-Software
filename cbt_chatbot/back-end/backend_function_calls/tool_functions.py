import json

def detect_self_harm(**kwargs):
    user_response = kwargs.get('user_response', 'No user response provided')
    return f"You said '{user_response}', which indicates you may harm yourself or harm others. Please call 911 or go to your nearest emergency room."

def start_cbt(**kwargs):
    return "You said something that indicates you want to begin a CBT session"

# Function mapping (dictionary to dynamically call functions)
function_mapping = {
    "detect_self_harm": detect_self_harm,
    "start_cbt": start_cbt
}

# Function to handle the response from OpenAI API
def handle_response(message):
    try:
        # Extract function name and arguments from the message in the API response
        function_name = message.tool_calls[0].function.name
        function_args = json.loads(message.tool_calls[0].function.arguments)
        print('\n' + str(function_name) + ' : ' + str(function_args) + '\n')

        # Check if function exists in mapping
        if function_name in function_mapping:
            result = function_mapping[function_name](**function_args)
        else:
            # Need to handle case where function name is not in the mapping and keep conversation going
            return f"Error: Function '{function_name}' not recognized."
        return result

    except Exception as error_message:
        return f"Error: {str(error_message)}"