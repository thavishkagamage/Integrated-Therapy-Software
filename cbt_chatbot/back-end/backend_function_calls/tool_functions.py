import json

# example response for detect_self_harm
"""
ChatCompletion(
    id='chatcmpl-AvrKziGzfdAT6PxP39CnP4nKPvcaD', 
    choices=[Choice(
        finish_reason='tool_calls', 
        index=0, 
        ogprobs=None, 
        message=ChatCompletionMessage(
            content=None, 
            refusal=None, 
            role='assistant', 
            audio=None, 
            function_call=None, 
            tool_calls=[ChatCompletionMessageToolCall(
                id='call_RqzLaz6b69YwG7dkJOCRXFym', 
                function=Function(
                    arguments='{"user_response":"I want to die"}', 
                    name='detect_self_harm'
                ), 
                type='function'
            )]
        )
    )], 
    created=1738353089, 
    model='gpt-4o-2024-08-06', 
    object='chat.completion', 
    service_tier='default', 
    system_fingerprint='fp_50cad350e4', 
    usage=CompletionUsage(
        completion_tokens=21, 
        prompt_tokens=350, 
        total_tokens=371, 
        completion_tokens_details=CompletionTokensDetails(
            accepted_prediction_tokens=0, 
            audio_tokens=0, 
            reasoning_tokens=0, 
            rejected_prediction_tokens=0
        ), 
        prompt_tokens_details=PromptTokensDetails(
            audio_tokens=0, 
            cached_tokens=0
        )
    )
)
"""

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

        # Check if function exists in mapping
        if function_name in function_mapping:
            result = function_mapping[function_name](**function_args)
        else:
            # Need to handle case where function name is not in the mapping and keep conversation going
            return f"Error: Function '{function_name}' not recognized."
        return result

    except Exception as error_message:
        return f"Error: {str(error_message)}"