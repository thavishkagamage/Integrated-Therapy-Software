# List of all tools

def get_all_tools(agenda_item):
  
  return [
    {
      "type": "function",
      "function": {
        "name": "detect_self_harm",
        "description": "Detects when user has a response that indicates self harm or harm to others in a therapy setting",
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
        "name": "start_cbt",
        "description": "Detects when user wants to begin a CBT session",
        "strict": True,
        "parameters": {
          "type": "object",
          "required": [
            "user_response"
          ],
          "properties": {
            "user_response": {
              "type": "string",
              "description": "Response from the user that indicates they want to begin a CBT session"
            }
          },
          "additionalProperties": False
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "complete_agenda_item",
        "description": f"This is the current agenda item: {agenda_item}. This tool should activate when you believe this current agenda item has been completed. Please use all conversation context to determine if this item has been completed.",
        "strict": True,
        "parameters": {
          "type": "object",
          "required": [
            "user_response"
          ],
          "properties": {
            "user_response": {
              "type": "string",
              "description": "Response from the user that indicates they want to begin a CBT session"
            }
          },
          "additionalProperties": False
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "update_current_agenda",
        "description": "select a new agenda item when none of the agenda items on the agenda item list are marked as current",
        "strict": True,
        "parameters": {
          "type": "object",
          "required": [
            "user_response"
          ],
          "properties": {
            "user_response": {
              "type": "string",
              "description": "Response from the user that indicates they want to begin a CBT session"
            }
          },
          "additionalProperties": False
        }
      }
    }
  ]