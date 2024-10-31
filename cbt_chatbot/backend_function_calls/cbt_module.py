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