from JsonWritingStrategy import *

import json
import os


class IncrementalJsonWritingStrategy(JsonWritingStrategy):
    def __init__(self):
        self.is_first_entry = True

    def write_json(self, data, filename):
        # Check if the file exists and its size is greater than zero (i.e., it's not empty)
        file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0

        with open(filename, 'a+', encoding='utf-8') as json_file:
            
            if not file_exists:
                json_file.write('[')
            else:
                # Move to the end of the file
                json_file.seek(0, os.SEEK_END)

                # If it's not the first entry, add a comma before the next JSON object
                if not self.is_first_entry:
                    json_file.write(',')
                else:
                    # Remove the closing bracket before appending next object
                    json_file.seek(-1, os.SEEK_END)
                    json_file.truncate()

            # Convert the data to a JSON string and write it
            formatted_json_string = json.dumps(data, ensure_ascii=False, indent=4)
            json_file.write(formatted_json_string)

            self.is_first_entry = False


    def closetab(self,filename):
        with open(filename, 'a') as file:
            file.write("]")


class BatchJsonWritingStrategy(JsonWritingStrategy):
    """
    to be implemented...
    """
    def __init__(self, batch_size=100):
        self.batch_size = batch_size
        self.batch_data = []

    def write_json(self, data, filename):
        self.batch_data.append(data)
        if len(self.batch_data) >= self.batch_size:
            with open(filename, 'a', encoding='utf-8') as json_file:
                self.batch_data = []
