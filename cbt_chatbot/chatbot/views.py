import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import json


#ai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data['message']
        
        # messages = [
        #     {"role": "user", "content": user_message},
        # ]
        # chat_completion = ai_client.chat.completions.create(
        #         messages=messages,
        #         model="gpt-3.5-turbo",
        #     )
        bot_response = f"Hello world: {user_message}" #chat_completion.choices[0].message.content

        return JsonResponse({'message': bot_response})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)