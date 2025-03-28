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


# reset current_sub_items for new agenda item, get new dictionary
def reset_current_sub_items(agenda_status, conversation_id):
    # update the conversation object with the new current_sub_items
    try:
        conversation = Conversation.objects.get(id=conversation_id)

        # session file retrieval/caching
        cache_key = f'session{conversation.session_number}'
        session_instructions_json = get_cache_file(cache_key)

        # get the actual agenda item instructions
        conversation_agenda_instructions = session_instructions_json.get("Current Agenda Item Instructions", [])
        current_item_instructions = conversation_agenda_instructions[agenda_status.index(1)]

        # Extract the "Current Agenda Item Instructions" and build the new list for the database
        # This will look like [1, 0, 0, ...]
        new_sub_items_status = [1 if i == 0 else 0 for i in range(len(current_item_instructions))]

        current_item_instructions_dict = zip_agenda_with_status(current_item_instructions, new_sub_items_status)

        conversation.current_sub_items = new_sub_items_status
        conversation.save(update_fields=['current_sub_items'])
    except Exception as error:
        print(f'ERROR: {error}\n')

    return current_item_instructions_dict

# changes the first instance of a 0 into a 1 in current_sub_items
def make_next_item_current(current_sub_item_statuses, conversation_id):
    first_zero_index = current_sub_item_statuses.index(0) # if 0 in current_sub_item_statuses else -1 NOT NEEDED
    current_sub_item_statuses[first_zero_index] = 1

    # update the conversation object with the new sub statuses
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        conversation.current_sub_items = current_sub_item_statuses
        conversation.save(update_fields=['current_sub_items'])
    except Exception as error:
        print(f'ERROR: {error}\n')

    return current_sub_item_statuses


# changes the first instance of a 1 into a 2 in the agenda
def make_current_item_complete(conversation_id):

    # update the conversation object with the new agenda statuses
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        agenda_status = conversation.agenda_items

        first_one_index = agenda_status.index(1) # if 1 in agenda_statuses else -1 NOT NEEDED
        agenda_status[first_one_index] = 2

        conversation.agenda_items = agenda_status
        conversation.save(update_fields=['agenda_items'])
    except Exception as error:
        print(f'ERROR: {error}\n')

    return agenda_status


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

    # session file retrieval/caching
    cache_key = f'session{session_number}'
    session_instructions_json = get_cache_file(cache_key)

    # get the agenda
    conversation_agenda = session_instructions_json.get("Conversation Agenda", [])
    
    # return agenda
    return JsonResponse({'agenda': conversation_agenda})