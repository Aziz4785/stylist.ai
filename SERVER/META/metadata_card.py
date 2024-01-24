from META.metadata_extractors_util import *

class MetaDataCard:
    def __init__(self, extractors):
        self.extractors = extractors
        self.metadata = {
            "type": "unknown",
            "composition_in": {"unknown"},
            "composition_out": {"unknown"},
            "contains_black": "unknown",
            "contains_white": "unknown",
            "contains_other_color": "unknown",
            "gender": "unknown"
        }

    def generate_from_query(self, query):
        self.metadata["type"] = self.extractors["type"].extract(query)
        self.metadata["composition_in"] ,self.metadata["composition_out"]= self.extractors["composition"].extract(query)
        self.metadata["contains_black"] ,self.metadata["contains_white"]= self.extractors["blackwhite"].extract(query)
        self.metadata["contains_other_color"]= self.extractors["otherColor"].extract(query)
        self.metadata["gender"]= self.extractors["gender"].extract(query)
        
    def __str__(self):
        return f"MetaDataCard({', '.join(f'{key}: {value}' for key, value in self.metadata.items())})"
