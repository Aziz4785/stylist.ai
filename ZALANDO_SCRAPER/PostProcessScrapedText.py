import json
import os
import re

def remove_SeeEnvironementSpec(json_file_path):
    pattern = "See environmental specifications"

    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        for key in item:
            if isinstance(item[key], str):
                item[key] = item[key].replace(pattern, "")

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
def remove_reference(json_file_path):
    # Regular expression pattern to match "Reference: " followed by any characters
    # stopping at a space, comma, point, or the end of the string
    pattern = r"Reference: [^ ,.]*[ ,.]?"

    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        for key in item:
            if isinstance(item[key], str):
                item[key] = re.sub(pattern, "", item[key])

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def add_incremental_id(json_file_path, last_id=0):
    with open(json_file_path, 'r' , encoding='utf-8') as file:
        data = json.load(file)

    current_id = last_id
    for item in data:
        current_id += 1
        hex_id = f"{current_id:06x}"  
        item['id'] = "#I"+hex_id

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return current_id

def post_process_json_files_in_folder(folder_path, operations):
    last_id = 3  # Starting ID in decimal
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            json_file_path = os.path.join(folder_path, filename)
            for operation in operations:
                if operation.__name__ == 'add_incremental_id':
                    last_id = operation(json_file_path, last_id)
                else:
                    operation(json_file_path)
        else:
            print(f"Skipping non-JSON file: {filename}")

folder_path = 'zalando_text_scraper/output_json' 
operations = [add_incremental_id, remove_reference, remove_SeeEnvironementSpec]
post_process_json_files_in_folder(folder_path, operations)