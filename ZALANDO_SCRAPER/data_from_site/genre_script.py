import json
def genrescript(filename):
    """
    Appends the given element to a JSON file.

    :param baseline_elem: The element to be added.
    :param filename: Name of the JSON file to which the element is added.
    """
    try:
        # Read the existing data from the file
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        for item in data:
            item['genre'] = 'men'

        # Write the updated data back to the file
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"An error occurred: {e}")

genrescript("data_streetwear-homme.json")