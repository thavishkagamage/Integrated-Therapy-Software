# cache files that contain our system prompt information

import os
import json
from django.conf import settings
from django.core.cache import cache

def get_system_prompt():
    
    # the cache key is how we get a specific file from our cached memory
    # we can set this dynamically o pass it in as an argument here to retrieve files
    cache_key = '?'

    # get file from cache
    prompts = cache.get(cache_key)

    # if file is not in our cache
    if prompts is None:

        # we can pass in a file name to determine what file to retrive if cache is empty
        file_name = 'prompts.json'
    
        # Construct the full file path to your JSON file
        file_path = os.path.join(settings.BASE_DIR, 'back-end', 'backend_function_calls', 'prompts', file_name)
        
        try:
            with open(file_path, 'r') as json_file:
                prompts = json.load(json_file)
            # Cache the prompts with a long timeout (or use None)
            cache.set(cache_key, prompts, timeout=60 * 60 * 24 * 365 * 10) # 10 years in seconds
        
        except FileNotFoundError:
            # Optionally, handle the error or re-raise an exception
            prompts = {}

    return prompts