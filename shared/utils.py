import json
import os

import bson
import numpy as np
import pytz
from datetime import datetime, time


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


def date_to_timestamp(date_obj: datetime.date) -> int:
    """Converts a date object to a Unix timestamp (seconds since epoch) at the start of that day."""
    # Convert date to datetime at the start of the day for timestamp conversion
    dt_obj = datetime.combine(date_obj, time.min)
    return int(dt_obj.timestamp())


def timestamp_to_date(ts: int) -> datetime.date:
    """Converts a Unix timestamp (seconds since epoch) to a date object."""
    return datetime.fromtimestamp(ts).date()


def parse_date_string(date_str: str) -> datetime.date:
    """Parses a 'YYYY-MM-DD' string into a date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def date_to_string(dt_obj: datetime.date) -> str:
    """Converts a datetime object to a string in the format 'YYYY-MM-DD'."""
    return dt_obj.strftime("%Y-%m-%d")


class graph_data:
    def __init__(self, title, url, description, raw_data):
        self.title = title
        self.url = url
        self.description = description
        self.raw_data = raw_data
