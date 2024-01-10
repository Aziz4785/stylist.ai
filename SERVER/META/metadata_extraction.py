from SERVER.META.metadata_extractors_util import *
from abc import ABC, abstractmethod

class IMetadataExtractor(ABC):
    @abstractmethod
    def extract(self, query):
        pass

class CompositionExtractor(IMetadataExtractor):
    def extract(self, query):
        result = extract_composition_in_out(gpt35_composition_output(query))
        #result = extract_composition_in_out(starling_composition_output(query))
        return result

class TypeExtractor(IMetadataExtractor):
    def extract(self, query):
        return extract_garment_type(gpt35_type_output(query))

class BlackWhiteExtractor(IMetadataExtractor):
    def extract(self, query):
        return extract_blackwhite(gpt35_bw_ouput(query))
    
class OtherColorExtractor(IMetadataExtractor):
    def extract(self, query):
        #return extract_otherColor(gpt35_otherColor_ouput(query))
        return extract_otherColor(starling_otherColor_ouput(query))
    
class GenreExtractor(IMetadataExtractor):
    def extract(self, query):
        return extract_genre(gpt35_genre_ouput(query))