import json
import os

import bson
import numpy as np
import pytz
from datetime import datetime

def generate_id():
    return str(bson.ObjectId())


def format_customer_name(name):
    if not name:
        return name

    # Remove extra whitespace and split into words
    words = name.strip().split()

    # Capitalize each word properly
    formatted_words = []
    for word in words:
        # Handle empty words
        if not word:
            continue

        # Special case for names with internal capitals like "McDonald"
        if len(word) > 2 and any(c.isupper() for c in word[1:]):
            # Preserve existing capitalization
            formatted_words.append(word)
        else:
            # Standard capitalization
            formatted_words.append(word.capitalize())
    return " ".join(formatted_words)

def asia_jakarta_time(value):
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    return value.astimezone(jakarta_tz)

def convert_to_utc(value):
    local_dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    local_dt_aware = jakarta_tz.localize(local_dt)
    utc_dt = local_dt_aware.astimezone(pytz.UTC)
    return utc_dt

def delete_file_graph(filename: str):
    if os.path.exists(filename):
        os.remove(filename)

def convert_numpy_for_json(data: dict) -> str:
    """
    Recursively convert NumPy types in a dict to native Python types,
    then return a JSON-formatted string.
    """
    def convert(obj):
        if isinstance(obj, dict):
            return {convert(k): convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(i) for i in obj]
        elif isinstance(obj, tuple):
            return tuple(convert(i) for i in obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.str_):
            return str(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj

    cleaned_data = convert(data)
    return json.dumps(cleaned_data, ensure_ascii=False, indent=2)


class graph_data:
    def __init__(self, title, url, description, raw_data):
        self.title = title
        self.url = url
        self.description = description
        self.raw_data = raw_data
