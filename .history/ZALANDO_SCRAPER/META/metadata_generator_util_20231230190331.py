import re
def extract_blackwhite(text):
    # Initialize the list with 'None' to indicate unfound words
    mylist = [None, None]

    # Function to find the first occurrence of 'yes' or 'no' in a given segment
    def find_yes_no(segment):
        if 'yes' in segment:
            return 'yes'
        elif 'no' in segment:
            return 'no'
        else:
            return None

    # Splitting text at 'black' and 'white'
    parts_black = text.split('black')
    parts_white = text.split('white')

    # Check for 'yes' or 'no' between 'black' and 'white'
    if len(parts_black) > 1:
        for i in range(1, len(parts_black)):
            segment = parts_black[i].split('white')[0] if 'white' in parts_black[i] else parts_black[i]
            mylist[0] = find_yes_no(segment)
            if mylist[0]:
                break

    # Check for 'yes' or 'no' between 'white' and 'black'
    if len(parts_white) > 1:
        for i in range(1, len(parts_white)):
            segment = parts_white[i].split('black')[0] if 'black' in parts_white[i] else parts_white[i]
            mylist[1] = find_yes_no(segment)
            if mylist[1]:
                break

    return mylist

def extract_otherColor(text):
    # Split the text by whitespace to get individual words
    print("text  from llm: ")
    print(text)
    print()
    pattern_yes = r'\byes\b'
    pattern_no = r'\bno\b'

    # Use regular expression to find all matches
    yes_count = len(re.findall(pattern_yes, text))
    no_count = len(re.findall(pattern_no, text))

    if(yes_count>no_count):
        return "yes"
    elif(yes_count==no_count):
        return "unknown"
    else:
        return "no"

def extract_garment_type(txt):
    categories = ["Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories", "One-Pieces","Other","unknown"]

    # Check if any of the keywords are in the text
    for category in categories:
        if category in txt:
            return category

    # Return "unknown" if no matching category is found
    return "unknown"


def extract_composition(txt):
    categories = ["synthetic", "natural", "artificial"]
    res = set()
    # Check if any of the keywords are in the text
    for category in categories:
        if category in txt:
            res.add(category)

    # Return "unknown" if no matching category is found
    return res

def remove_artificial_fabric(text):
    words_to_replace = ["viscose", "acetate", "rayon", "Viscose", "Acetate", "Rayon"]
    found = False
    new_text = text

    for word in words_to_replace:
        if word in new_text:
            found = True
            new_text = new_text.replace(word, "unknown")

    return found, new_text