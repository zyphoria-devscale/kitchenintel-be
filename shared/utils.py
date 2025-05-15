import bson


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