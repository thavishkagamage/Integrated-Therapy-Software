class ChatMode:
    def __init__(self, initial_mode="fc_general"):
        """
        Initialize a ChatMode instance with a specific mode.

        Args:
            initial_mode (str): The starting mode of the chatbot. Defaults to "fc_general".
        
        Raises:
            ValueError: If the provided initial mode is not valid.
        """
        if initial_mode not in self.mode_attributes:
            raise ValueError(f"Invalid initial mode '{initial_mode}'. Available modes: {list(self.mode_attributes.keys())}")
        
        self.current_mode = initial_mode
        self.conversation_state = {
            "mode": self.current_mode,
            "history": []  # To store user interactions and function calls
        }

    # Shared functionality for overlapping modes
    shared_functions = {
        "get_user_mood": {
            "name": "get_user_mood",
            "description": "Get the user's current mood.",
            "parameters": {
                "mood": {
                    "type": "string",
                    "description": "User's mood.",
                    "enum": ["happy", "sad", "despair", "numb"]
                }
            }
        }
    }

    # Mode-specific attributes
    mode_attributes = {
        "fc_general": {
            "goal": "Identify the user's needs.",
            "functions": {
                "name": "goal_identified",
                "description": "Identify user goals based on input.",
                "parameters": {
                    "goal": {"type": "string", "description": "The identified goal for the user."}
                }
            }
        },
        "cbt_goal_setting": {
            "goal": "Help the user set actionable therapy goals.",
            "functions": shared_functions["get_user_mood"]
        }
    }

    # Rules for transitioning between modes
    transition_rules = {
        "fc_general": {
            "goal_identified": "cbt_goal_setting",
            "default": "fc_general"
        },
        "cbt_goal_setting": {
            "goal_completed": "fc_general",
            "default": "cbt_goal_setting"
        }
    }

    def get_mode_instructions(self):
        """
        Fetch and format instructions for the current mode.

        Returns:
            dict: Instructions for the current mode, including the goal and functions.
        """
        attributes = self.mode_attributes.get(self.current_mode)
        if not attributes:
            return {"error": f"Mode '{self.current_mode}' not found."}

        return {
            "mode": self.current_mode,
            "goal": attributes["goal"],
            "functions": attributes["functions"]
        }

    def switch_mode(self, new_mode):
        """
        Switch the current mode of the chatbot.

        Args:
            new_mode (str): The new mode to switch to.
        
        Raises:
            ValueError: If the new mode is not valid.
        """
        if new_mode not in self.mode_attributes:
            raise ValueError(f"Invalid mode '{new_mode}'. Available modes: {list(self.mode_attributes.keys())}")
        
        self.current_mode = new_mode
        self.conversation_state["mode"] = new_mode
        print(f"Switched to mode: {new_mode}")

    def get_next_mode(self, current_mode, event):
        """
        Determine the next mode based on the current mode and event.

        Args:
            current_mode (str): The current mode.
            event (str): The event triggering a transition.

        Returns:
            str: The next mode.
        """
        return self.transition_rules.get(current_mode, {}).get(event, self.transition_rules[current_mode]["default"])

    def process_function_call(self, function_name, args):
        """
        Process a function call returned from OpenAI API.

        Args:
            function_name (str): Name of the function being called.
            args (dict): Arguments provided by the function call.
        """
        print(f"Processing function: {function_name} with arguments: {args}")

        # Validate the function arguments
        if not self.validate_function_args(function_name, args):
            print(f"Invalid arguments provided for function: {function_name}")
            return

        # Trigger a mode switch if applicable
        next_mode = self.get_next_mode(self.current_mode, function_name)
        if next_mode != self.current_mode:
            self.switch_mode(next_mode)

    def validate_function_args(self, function_name, args):
        """
        Validate the arguments provided for a function call.

        Args:
            function_name (str): The name of the function.
            args (dict): The arguments provided.

        Returns:
            bool: True if valid, False otherwise.
        """
        function_details = self.mode_attributes.get(self.current_mode, {}).get("functions")
        if not function_details or function_details["name"] != function_name:
            return False

        required_params = function_details.get("parameters", {})
        for param, details in required_params.items():
            if param not in args or not isinstance(args[param], eval(details["type"])):
                return False
        return True

    def log_interaction(self, user_input, response, function_call=None):
        """
        Log user interaction and chatbot response.

        Args:
            user_input (str): The user's input.
            response (str): The chatbot's response.
            function_call (dict): Details of the function call, if any.
        """
        self.conversation_state["history"].append({
            "user_input": user_input,
            "response": response,
            "function_call": function_call
        })

    def suggest_function_call(self):
        """
        Suggest the appropriate function call based on the current mode.

        Returns:
            dict: Suggested function details.
        """
        attributes = self.mode_attributes.get(self.current_mode)
        if not attributes:
            return {"error": f"Mode '{self.current_mode}' not found."}
        return attributes["functions"]


# Backend Logic to Handle OpenAI Responses
def handle_openai_response(chat_mode, response):
    """
    Handle a response from OpenAI's API.

    Args:
        chat_mode (ChatMode): The ChatMode instance managing the state.
        response (dict): The API response, including function calls and arguments.
    """
    function_call = response.get("function_call")
    if function_call:
        function_name = function_call["name"]
        args = function_call.get("arguments", {})
        chat_mode.process_function_call(function_name, args)

    print(f"Current Mode: {chat_mode.current_mode}")
    print("Suggested Function:", chat_mode.suggest_function_call())


# Example Usage
if __name__ == "__main__":
    # Initialize the chat mode
    chat_mode = ChatMode("fc_general")

    # Mock OpenAI API response
    mock_response = {
        "function_call": {
            "name": "goal_identified",
            "arguments": {"goal": "Set therapy goals"}
        }
    }

    # Handle the response and switch modes if needed
    handle_openai_response(chat_mode, mock_response)

    # Display the current mode instructions
    print("\nMode Instructions:")
    print(chat_mode.get_mode_instructions())

    # Suggest the next function call
    print("\nNext Suggested Function Call:")
    print(chat_mode.suggest_function_call())
