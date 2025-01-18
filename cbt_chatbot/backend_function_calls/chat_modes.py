# Owner: Thavishka Gamage
# Purpose: Defines the instructions for different chat modes with modular instruction components

class ChatMode:
    def __init__(self, mode):
        """
        Initialize a ChatMode instance with a specific mode.
        """
        self.mode = mode

    # Identity - Who does it believe it is?
    identity = {
        "ex_identity": "You are a mental health chatbot."
    }

    # Purpose - Why does it believe it exists?
    purpose = {
        "ex_purpose": "You exist to help a user."
    }

    # Behavior - Relevant behavior and personality traits
    behavior = {
        "ex_behavior": "You are well-behaved, polite, conversational, and friendly."
    }

    # Goals - The objectives for the chatbot in different modes
    goal = {
        "fc_ex_goal": "You must convince the user to eat chocolate chip cookies.",
        "cbt_invitation_goal": "You must invite the user to join Cognitive Behavioral Therapy (CBT) sessions.",
        "cbt_goal_setting_goal": "Help the user set realistic and actionable therapy goals."
    }

    # Voice - How it talks
    voice = {
        "ex_voice": "You speak like a calm and collected Midwestern high school boy."
    }

    # Format - Response formatting
    format = {
        "ex_format": "You give responses that are a couple of sentences in length, like a person talking in a conversation."
    }

    # Guardrails - What should it not do?
    guardrail = {
        "ex_guardrail": "You do not give legal, medical, or financial advice."
    }

    # Functions - Specific actions the chatbot can perform
    functions = {
        "ex_function": {
            "name": "ex_function",
            "description": "Get how the user is feeling, with options for how long. Do this if they indicate they are not doing well.",
            "parameters": {
                "mood": {
                    "type": "string",
                    "description": "How the user is feeling.",
                    "enum": ["happy", "sad", "despair", "numb"]
                },
                "duration": {
                    "type": "int",
                    "description": "How long the user has been feeling this way, in days."
                }
            },
            "required": ["mood"],
            "additionalProperties": False
        }
    }

    # Mode attributes - Combined instructions for each mode
    mode_attributes = {
        # Free Chat Modes
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
        # CBT Modes
        "cbt_invitation": {
            "identity": identity["ex_identity"],
            "purpose": purpose["ex_purpose"],
            "behavior": behavior["ex_behavior"],
            "goal": goal["cbt_invitation_goal"],
            "voice": voice["ex_voice"],
            "format": format["ex_format"],
            "guardrail": guardrail["ex_guardrail"],
            "functions": functions["ex_function"]
        },
        "cbt_goal_setting": {
            "identity": identity["ex_identity"],
            "purpose": purpose["ex_purpose"],
            "behavior": behavior["ex_behavior"],
            "goal": goal["cbt_goal_setting_goal"],
            "voice": voice["ex_voice"],
            "format": format["ex_format"],
            "guardrail": guardrail["ex_guardrail"],
            "functions": functions["ex_function"]
        }
    }

    def get_mode_instructions(self, mode):
        """
        Fetch and format instructions for a specific mode.

        Args:
            mode (str): The mode for which instructions are required.

        Returns:
            tuple: A formatted string of instructions and the mode's functions.
        """
        attributes = self.mode_attributes.get(mode)
        if not attributes:
            return f"Mode '{mode}' not found.", None

        instructions = (
            f"Identity: {attributes['identity']}\n"
            f"Purpose: {attributes['purpose']}\n"
            f"Behavior: {attributes['behavior']}\n"
            f"Goal: {attributes['goal']}\n"
            f"Voice: {attributes['voice']}\n"
            f"Format: {attributes['format']}\n"
            f"Guardrail: {attributes['guardrail']}\n"
        )
        return instructions, attributes['functions']


# Test function
def test_get_mode_instructions():
    """
    Interactive test function for ChatMode.
    """
    # Create an instance of ChatMode
    chat_mode = ChatMode("mental_health_assistant")

    while True:
        # Prompt user to enter a mode or type 'exit' to quit
        mode = input("Enter the mode you want to test (or type 'exit' to quit): ").strip()
        if mode.lower() == 'exit':
            print("Exiting test.")
            break

        # Get the instructions for the entered mode
        instructions, functions = chat_mode.get_mode_instructions(mode)
        print("\n--- Requested Mode Instructions ---")
        print(instructions)
        print("Functions:", functions)
        print("-" * 50)  # Separator for readability


# Run the interactive test function
if __name__ == "__main__":
    test_get_mode_instructions()
