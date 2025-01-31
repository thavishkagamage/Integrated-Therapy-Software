tools = [
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
  }
]