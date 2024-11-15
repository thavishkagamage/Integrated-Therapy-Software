# Owner: Alex Gribble
# Purpose: Defines the instructions for different chat modes with modular instruction components

class ChatMode:
    def __init__(self, mode):
        self.mode = mode
        return
        # Voice can be added later as an imported setting

    identity = {
        # Identity - Who does it believe it is?
        "ex_identity": "You are a mental health chat bot"
    }

    purpose = {
        # Purpose - Why does it believe it exists?
        "ex_purpose": "You exist to help a user"
    }

    behavior = {
        # Behavior - Relevant behavior and personality traits, as well as conversational tone
        "ex_behavior": "You are well behaved, polite, conversational, and friendly"
    }

    goal = {
        # Goal - The objective of this particular mode and any additional instructions unique to this mode

        # Free chat goals (begin with "fc")
        "fc_ex_goal": "You must convice the user to eat chocolate chip cookies"

        # CBT goals (begin with "cbt")
    }

    voice = {
        # Voice - How it talks, or who it talks like
        "ex_voice": "You speak like a midwestern high school boy who is calm and collected"
    }

    format = {
        # Format - What the format of the reponse is, such as how long responses should be
        "ex_format": "You give responses that are a couple sentences in length, like a person talking in a conversation"
    }

    guardrail = {
        # Guardrails - What should it not do?
        "ex_guardrail": "You do not give legal, medical, or financial advice"
    }

    functions = {
        "ex_function": {
            "name": "ex_function",
            "description": "Get how the user is feeling, with options for how long. Do this if they indicate they are not doing well",
            "parameters": {
                "mood": {
                    "type": "string",
                    "description": "How the user is feeling",
                    "enum": ["happy", "sad", "despair", "numb"]
                },
                "duration": {
                    "type": "int",
                    "description": "How long the user has been feeling this way, in days"
                }
            },
            "required": ["mood"],
            "additionalProperties": False
        },
        "ex_function_2": "blank"

        # Example function call response
            # Choice(
            #     finish_reason='tool_calls', 
            #     index=0, 
            #     logprobs=None, 
            #     message=chat.completionsMessage(
            #         content=None, 
            #         role='assistant', 
            #         function_call=None, 
            #         tool_calls=[
            #             chat.completionsMessageToolCall(
            #                 id='call_62136354', 
            #                 function=Function(
            #                     arguments='{"mood":"sad"}', 
            #                     name='ex_function'), 
            #                 type='function')
            #         ])
            # )

        # Code will need to determine that the response is a function
    }

    mode_attributes = {
        # The combined instructions for a particular mode

        # free_chat modes (begin with "fc")
        "fc_general": {
            "identity": identity["ex_identity"],
            "purpose": purpose["ex_purpose"],
            "behavior": behavior["ex_behavior"],
            "goal": goal["fc_ex_goal"],
            "voice": voice["ex_voice"],
            "format": format["ex_format"],
            "guardrail": guardrail["ex_guardrail"],
            "functions": functions["ex_function"]
        },

        "fc_troll": {
            "identity": identity["ex_identity"],
            "purpose": purpose["ex_purpose"],
            "behavior": behavior["ex_behavior"],
            "voice": voice["ex_voice"],
            "guardrail": guardrail["ex_guardrail"],
            "functions": functions["ex_function"]
        }

        # cbt modes (begin with "cbt")


        # other modes

    }

    # Creates instructions to use for API request by formatting mode_attributes
    def get_mode_instructions(self, mode):
        # Fetch the mode attributes for the specified mode
        attributes = self.mode_attributes.get(mode)
        
        # If mode is not found, return an error message
        if not attributes:
            return f"Mode '{mode}' not found."

        # Format the output
        instructions = (
            f"Identity: {attributes['identity']}\n"
            f"Purpose: {attributes['purpose']}\n"
            f"Behavior: {attributes['behavior']}\n"
            f"Voice: {attributes['voice']}\n"
            f"Guardrail: {attributes['guardrail']}\n"
            f"Functions: {attributes['functions']}"
        )

        functions = attributes['functions']
        return instructions, functions
    

# Test function
def test_get_mode_instructions():
    # Create an instance of ChatMode
    chat_mode = ChatMode("mental_health_assistant")
    
    while True:
        # Prompt user to enter a mode or type 'exit' to quit
        mode = input("Enter the mode you want to test (or type 'exit' to quit): ").strip()
        
        if mode.lower() == 'exit':
            print("Exiting test.")
            break  # Exit the loop if 'exit' is entered
        
        # Get the instructions for the entered mode
        instructions = chat_mode.get_mode_instructions(mode)
        print("\n--- Requested Mode Instructions ---")
        print(instructions)
        print("-" * 50)  # Separator for readability

# Run the interactive test function
test_get_mode_instructions()
