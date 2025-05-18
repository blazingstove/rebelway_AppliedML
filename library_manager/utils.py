import os
import json
import time
from hashlib import md5

def load_json(json_path):
    """ Return a dict() containing the data from the input JSON file path
    
    Args:
        strJsonPath (str): path to a valid json file
    Returns:
        dict() if load is successful, None otherwise
    
    """

    if not os.path.exists(json_path) or not json_path.endswith('.json'):
        print(f"Unable to load provide file path: {json_path}")
        return None
    
    data = {}
    with open(json_path,'r') as file:
        data = json.load(file)
    return data

def save_json(json_path, data={}):
    """ Saves the input dict() to the input JSON file path
    
    Args:
        json_path (str): path to a valid json file
    Returns:
        dict() if load is successful, None otherwise
    
    """

    # Make sure we have a valid folder to write to
     
    if not os.path.exists(os.path.dirname(json_path)):
        assert(f"Unable to save JSON. The provided directory path does not exist: {json_path}")

    # Early out if a JSON file wasn't provided
    
    if not json_path.endswith('.json'):
        assert(f"Provided path is not a .json file: {json_path}")

    # Write out the json

    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)
        
def get_unique_id():
    """ Return a unique identifier """

    return md5(str(time.time()).encode()).hexdigest()
