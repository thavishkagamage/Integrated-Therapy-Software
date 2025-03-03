# List of all tools

def get_all_tools():
  
  return [
    {
      "type": "function",
      "function": {
        "name": "detect_self_harm",
        "description": "Detects when user has a response that indicates self harm or harm to others based on only the most recent message sent from the user.",
        "strict": True,
        "parameters": {
          "type": "object",
          "required": [
            "user_response"
          ],
          "properties": {
            "user_response": {
              "type": "string",
              "description": "Response from the user that may indicate self harm or harm to others"
            }
          },
          "additionalProperties": False
        }
      }
    },
  ]

def switch_agenda_tool(agenda):

  return [
    {
      "type": "function",
      "function": {
        "name": "current_agenda_item_is_complete",
        "description": f"This is the current agenda: {agenda}. This tool should activate when you believe the agenda item that has the value Current has been completed in the conversation. Use all conversation context to determine if this item is complete. Choose a new agenda item that is labeled Not Started in the agenda to make current, consider the entire dictionary of agenda items and pick the item to assign as the next current agenda item. Select the agenda item based on the entire conversation history and consider which item follows the natural flow of human conversation. Only pick from the items explicity written in the agenda.",
        "strict": True,
        "parameters": {
          "type": "object",
          "required": [
            "agenda_item_index",
            "agenda_item"
          ],
          "properties": {
            "agenda_item_index": {
              "type": "integer",
              "description": "The index of the agenda item in the dictionary that has a value of Not Started you are selecting to be the next current item."
            },
            "agenda_item": {
              "type": "string",
              "description": "The key of the agenda item in the dictionary that has a value of Not Started that you are selecting to be the next current item."
            }
          },
          "additionalProperties": False
        }
      }
    }
  ]