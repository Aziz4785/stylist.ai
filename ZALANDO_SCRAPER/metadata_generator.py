import openai
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
openai.api_key = config.OPENAI_API_KEY

def extract_garment_type(txt):
    categories = ["Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories", "One-Pieces", "unknown"]

    # Check if any of the keywords are in the text
    for category in categories:
        if category in txt:
            return category

    # Return "unknown" if no matching category is found
    return "unknown"
def classify_garment_type(description):
    """
    Classify the type of a garment based on its text description.
    """

    prompt = f"Based on the following description, determine (in about 5 words) the garment type: Tops, Bottoms, Outerwear, Underwear, Footwear, Accessories, One-Pieces, unknown.\n\nDescription: {description}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or the most appropriate model you have access to
        messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                      {"role": "user", "content": prompt}],
        max_tokens=60
    )
    # Extract and return the garment type from the response
    garment_type = extract_garment_type(response.choices[0].message['content'])

    # Validate the garment type to ensure it's one of the predefined types
    valid_types = ["Tops", "Bottoms", "Outerwear", "Underwear", "Footwear", "Accessories", "One-Pieces", "unknown"]
    return garment_type if garment_type in valid_types else "unknown"

