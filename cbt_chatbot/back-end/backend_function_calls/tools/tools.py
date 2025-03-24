# List of all tools

def get_all_tools(agenda_item):
  
  return [
    {
      "type": "function",
      "function": {
        "name": "detect_self_harm",
        "description": "Use this tool to detect when a user expresses suicidal desire, including clear thoughts of ending their life, feeling trapped, hopeless, helpless, or like an unbearable burden. Only activate when distress is explicitly tied to suicide, self-harm, or a belief that suffering is permanent and escape is impossible. Do not trigger for vague sadness, stress, or emotional pain alone.",
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
    {
      "type": "function",
      "function": {
        "name": "current_agenda_item_is_complete",
        "description": f"This is the current agenda item: {agenda_item}. This tool should activate when you believe this current agenda item has been completed. Please use all conversation context to determine if this item has been completed.",
        "strict": True,
        "parameters": {
          "type": "object",
          "required": [], # Include this if the tool has no arguments
          "properties": {},
          "additionalProperties": False
        }
      }
    },
  ]

pick_new_agenda_item = [
  {
    "type": "function",
    "function": {
      "name": "pick_new_current_agenda_item",
      "description": "When the user wants to pick a new agenda item, choose a new agenda item that is not started to make current, consider the entire dictionary of agenda items and pick the item to assign as the next current agenda item. Make your selection of the agenda item based on the entire conversation history and consider which item follows the natural flow of human conversation.",
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
            "description": "The index of the agenda item in the dictionary that you are selecting to be the next current item."
          },
          "agenda_item": {
            "type": "string",
            "description": "The key of the agenda item in the dictionary that you are selecting to be the next current item."
          }
        },
        "additionalProperties": False
      }
    }
  }
]