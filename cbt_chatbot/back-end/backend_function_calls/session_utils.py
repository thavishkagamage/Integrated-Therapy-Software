# cache files that contain our system prompt information

import os
import json
from django.http import JsonResponse
from conversation_handler.models import Conversation
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from enum import Enum

GREEN = "\033[32m"
RESET = "\033[0m"

class AgendaStatus(Enum):
    Not_Started = 0
    Current = 1
    Complete = 2


# fetch the conversation object using the id
def get_conversation_object(conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return JsonResponse({'ERROR': 'Conversation not found'}, status=404)
    return conversation


# zips array of agenda items with array of statuses
# EX: {'Welcome the user': 'Current', 'Learn about user': 'Not Started', ...}
def zip_agenda_with_status(agenda_items, statuses):
    zipped_agenda = {
        item: AgendaStatus(status).name.replace("_", " ")
        for item, status in zip(agenda_items, statuses)
    }
    return zipped_agenda


def get_cache_file(cache_key):
    """
    Attempts to retrieve a file from the cache. If file is not in the cache, cache the file.
    Args:
        cache_key (str): identifier of the file in the cache (SAME AS FILE NAME without extension)
                        the cache key is how we get a specific file from our cached memory
    Returns:
        prompts (json): The content of the json file contianing the prompts
    """

    # get file from cache
    prompts = cache.get(cache_key)

    # if file is not in our cache
    if prompts is None:
        print(f'{GREEN}CHACHING:{RESET} Attempting to cache {cache_key}.json\n')

        # build file name from cache key
        file_name = f'{cache_key}.json'

        # Construct the full file path to your JSON file
        # BASE_DIR = /Integrated-Therapy-Software/cbt_chatbot/back-end
        file_path = os.path.join(settings.BASE_DIR, 'backend_function_calls', 'prompts', file_name)
        
        try:
            with open(file_path, 'r') as json_file:
                prompts = json.load(json_file)

            # Cache the file with a long timeout (or use None)
            cache.set(cache_key, prompts, timeout=60 * 60 * 24 * 365 * 10) # 10 years in seconds

            print(f'{GREEN}CHACHING:{RESET} {cache_key}.json is now in the cache\n')
        
        except Exception as error:
            # Optionally, handle the error or re-raise an exception
            print(f'ERROR: {error}\n')
            prompts = {}

    return prompts


@csrf_exempt
def get_agenda_items(request):
    data = json.loads(request.body)
    session_number = data.get('session_number')

    return JsonResponse({'session_number': session_number})