# cache files that contain our system prompt information

import os
import json
from django.conf import settings
from django.core.cache import cache

def get_cache_file(cache_key):
    """
    Attempts to retrieve a file from the cache. If file is not in the cache, cache the file.
    Args:
        cache_key (str): identifier of the file in the cache (SAME AS FILE NAME without extension)
    Returns:
        prompts (json): The content of the json file contianing the prompts
    """
    
    # the cache key is how we get a specific file from our cached memory
    # we can set this dynamically using DB values and pass it in as an argument here to retrieve files

    # get file from cache
    prompts = cache.get(cache_key)

    # if file is not in our cache
    if prompts is None:
        print(f'DEBUG: Adding {cache_key}.json to the cache')

        # build file name from cache key
        file_name = f'{cache_key}.json'

        # Construct the full file path to your JSON file
        # BASE_DIR = /Integrated-Therapy-Software/cbt_chatbot/back-end
        file_path = os.path.join(settings.BASE_DIR, 'backend_function_calls', 'static', file_name)
        
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