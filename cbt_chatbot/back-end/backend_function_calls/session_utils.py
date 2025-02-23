# cache files that contain our system prompt information

import os
import json
from django.conf import settings
from django.core.cache import cache
from enum import Enum


class AgendaStatus(Enum):
    Unstarted = 0
    Current = 1
    Completed = 2


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
        print(f'DEBUG: Adding {cache_key}.json to the cache')

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

            print(f'DEBUG: {cache_key}.json is now in the cache')
        
        except Exception as error:
            # Optionally, handle the error or re-raise an exception
            print('ERROR: {error}')
            prompts = {}

    return prompts