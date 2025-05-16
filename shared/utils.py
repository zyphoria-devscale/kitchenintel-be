import bson
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