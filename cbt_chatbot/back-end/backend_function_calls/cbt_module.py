class CBTModule:
    def __init__(self):
        # Initialize with available CBT types and their corresponding system prompts
        self.cbt_types = {
            'cognitive_restructuring': "You are a cognitive restructuring expert.",
            'exposure_therapy': "You are an exposure therapy expert.",
            'behavioral_activation': "You are a behavioral activation expert."
        }
        self.current_cbt_type = None

    def choose_cbt_type(self, cbt_type):
        """
        Choose the type of CBT.
        
        Args:
            cbt_type (str): The type of CBT to choose.
        
        Returns:
            str: Confirmation message or error message if the CBT type is invalid.
        """
        if cbt_type in self.cbt_types:
            self.current_cbt_type = cbt_type
            return f"CBT type '{cbt_type}' selected."
        else:
            return "Invalid CBT type. Please choose a valid type."

    def get_system_prompt(self):
        """
        Get the system prompt for the chosen CBT type.
        
        Returns:
            str: The system prompt for the chosen CBT type or an error message if no type is chosen.
        """
        if self.current_cbt_type:
            return self.cbt_types[self.current_cbt_type]
        else:
            return "No CBT type chosen. Please choose a CBT type first."

    def retrieve_journal_info(self, journal):
        """
        Retrieve information from the journal.
        
        Args:
            journal (Journal): The journal object to retrieve information from.
        
        Returns:
            str: Information retrieved from the journal.
        """
        # Assuming the journal object has a method get_entries() that returns journal entries
        return journal.get_entries()

# Example usage
if __name__ == "__main__":
    cbt_module = CBTModule()
    print(cbt_module.choose_cbt_type('cognitive_restructuring'))
    print(cbt_module.get_system_prompt())
    # Assuming we have a Journal class with a method get_entries()
    # journal = Journal()
    # print(cbt_module.retrieve_journal_info(journal))


# STARTER CODE FOR AGENDA
# not integrated -- not sure where to include this

# agenda_items = {
#     "Get the user to say the word sad":False,
#     "make the user say poop":False,
#     "get the user to mention tiananmen square":False,
# }

# Update T/F for agenda items
# def update_agenda_status(message, agenda_status):
#     for item in agenda_status.keys():
#         if item.lower() in message.lower():
#             agenda_status[item] = True
#     return agenda_status

# agenda_status = update_agenda_status(user_message, agenda_items)
        
# completed_items = [item for item, status in agenda_status.items() if status]
# remaining_items = [item for item, status in agenda_status.items() if not status]

# instructions = (
#         "You have the purpose of completing agenda items based on a structured agenda. The current agenda includes the following items: \n"
#         + "\n".join([f"- {item}" for item in agenda_items]) +
#         "\n\nHere is the current progress:\n"
#         + "Completed items:\n" + ("\n".join(completed_items) if completed_items else "None") +
#         "\n\nRemaining items:\n" + ("\n".join(remaining_items) if remaining_items else "None") +
#         "\n\nThe user's message is: \"{}\"\n".format(user_message) +
#         "Please provide a response that acknowledges the user's message and guides the conversation to address the next remaining agenda item. If all items are complete, please let the user know all agenda items are complete"
#     )
