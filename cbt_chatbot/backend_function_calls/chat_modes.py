class ChatMode:
    def __init__(self, initial_mode="fc_general"):
        """
        Initialize a ChatMode instance with a specific mode.

        Args:
            initial_mode (str): The starting mode of the chatbot. Defaults to "fc_general".
        
        Raises:
            ValueError: If the provided initial mode is not valid.
        """
        # Ensure the provided initial mode exists in the mode_attributes dictionary
        if initial_mode not in self.mode_attributes:
            raise ValueError(f"Invalid initial mode '{initial_mode}'. Available modes: {list(self.mode_attributes.keys())}")
        
        # Set the current mode of the chatbot
        self.current_mode = initial_mode
        
        # Initialize the conversation state, storing the current mode and chat history
        self.conversation_state = {
            "mode": self.current_mode,
            "history": []  # Chat history will be tracked here
        }

    # Identity - Defines who the chatbot believes it is
    identity = {
        "ex_identity": "You are a mental health chatbot."
    }

    # Purpose - Defines why the chatbot exists
    purpose = {
        "ex_purpose": "You exist to help a user."
    }

    # Behavior - Specifies the chatbot's personality and conversational tone
    behavior = {
        "ex_behavior": "You are well-behaved, polite, conversational, and friendly."
    }

    # Goals - The objectives for the chatbot in different modes
    goal = {
        "fc_ex_goal": "You must convince the user to eat chocolate chip cookies.",
        "cbt_invitation_goal": "You must invite the user to join Cognitive Behavioral Therapy (CBT) sessions.",
        "cbt_goal_setting_goal": "Help the user set realistic and actionable therapy goals."
    }

    # Voice - Specifies how the chatbot talks
    voice = {
        "ex_voice": "You speak like a calm and collected Midwestern high school boy."
    }

    # Format - Specifies the response style of the chatbot
    format = {
        "ex_format": "You give responses that are a couple of sentences in length, like a person talking in a conversation."
    }

    # Guardrails - Defines what the chatbot should not do
    guardrail = {
        "ex_guardrail": "You do not give legal, medical, or financial advice."
    }

    # Functions - Defines specific actions the chatbot can perform
    functions = {
        "ex_function": {
            "name": "ex_function",
            "description": "Get how the user is feeling, with options for how long. Do this if they indicate they are not doing well.",
            "parameters": {
                "mood": {
                    "type": "string",
                    "description": "How the user is feeling.",
                    "enum": ["happy", "sad", "despair", "numb"]  # Allowed values for mood
                },
                "duration": {
                    "type": "int",
                    "description": "How long the user has been feeling this way, in days."
                }
            },
            "required": ["mood"],  # Specifies required parameters
            "additionalProperties": False  # Disallows extra parameters
        }
    }

    # Mode attributes - Combines all instructions for each mode
    mode_attributes = {
        # General free chat mode
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
        # CBT invitation mode
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
        # CBT goal-setting mode
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

    def get_mode_instructions(self):
        """
        Fetch and format instructions for the current mode.

        Returns:
            tuple: A formatted string of instructions and the mode's functions.
        """
        # Retrieve attributes for the current mode
        attributes = self.mode_attributes.get(self.current_mode)
        if not attributes:
            return f"Mode '{self.current_mode}' not found.", None

        # Format and return the instructions as a string
        instructions = (
            f"Identity: {attributes['identity']}\n"
            f"Purpose: {attributes['purpose']}\n"
            f"Behavior: {attributes['behavior']}\n"
            f"Goal: {attributes['goal']}\n"
            f"Voice: {attributes['voice']}\n"
            f"Format: {attributes['format']}\n"
            f"Guardrail: {attributes['guardrail']}\n"
        )
        return instructions, attributes["functions"]

    def switch_mode(self, new_mode):
        """
        Switch to a different mode and update conversation state.

        Args:
            new_mode (str): The new mode to switch to.
        
        Raises:
            ValueError: If the new mode is not valid.
        """
        # Validate the new mode
        if new_mode not in self.mode_attributes:
            raise ValueError(f"Invalid mode '{new_mode}'. Available modes: {list(self.mode_attributes.keys())}")
        
        # Update the current mode and conversation state
        self.current_mode = new_mode
        self.conversation_state["mode"] = new_mode
        print(f"Switched to mode: {new_mode}")

    def suggest_function_call(self):
        """
        Suggest the appropriate function call based on the current mode.

        Returns:
            dict: Suggested function details.
        """
        # Retrieve attributes for the current mode
        attributes = self.mode_attributes.get(self.current_mode)
        if not attributes:
            raise ValueError(f"Mode '{self.current_mode}' not found.")
        return attributes["functions"]


# Test function
def test_mode_switching():
    """
    Test the mode switching functionality of the ChatMode class.
    """
    # Create a ChatMode instance with the default mode
    chat_mode = ChatMode("fc_general")
    print("Current Mode:", chat_mode.current_mode)
    print(chat_mode.get_mode_instructions())

    # Switch to a different mode
    chat_mode.switch_mode("cbt_goal_setting")
    print("After Switching Mode:", chat_mode.current_mode)
    print(chat_mode.get_mode_instructions())
    print("Suggested Function Call:", chat_mode.suggest_function_call())


# Run the test function if this file is executed directly
if __name__ == "__main__":
    test_mode_switching()
