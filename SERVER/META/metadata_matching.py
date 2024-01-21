from abc import ABC, abstractmethod
from META.metadata_utils import *
from common_variables import *
class IMetadataMatcher(ABC):
    @abstractmethod
    def is_match(self, json_elem, metadata_card):
        pass

class TypeMatcher(IMetadataMatcher):
    def is_match(self, json_elem, metadata_card):
        """
        return True if metadata_card and json_elem match on type
        """
        if json_elem is None:
            print("error in is_type_match ")
            return False
        
        if "type" not in json_elem:
            return True
        if(json_elem["type"]==""):
            return True
        if metadata_card.metadata["type"] is None or metadata_card.metadata["type"] =="":
            return True
        if(json_elem["type"] in corresponding_categories[metadata_card.metadata["type"]]):
            return True
        return False

class CompositionMatcher(IMetadataMatcher):
    def is_match(self, json_elem, metadata_card):
        """
        return True if metadata_card and json_elem match on composition
        """
        if "composition" not in json_elem  or json_elem["composition"]=="" or json_elem["composition"]=="unknown":
            return True
        if (metadata_card.metadata["composition_in"] is None or metadata_card.metadata["composition_in"] =="") and (metadata_card.metadata["composition_out"] is None or metadata_card.metadata["composition_out"] ==""):
            return True
        
        composition_of_json = convert_to_set(json_elem["composition"])
        composition_in_set = metadata_card.metadata["composition_in"]
        composition_out_set = metadata_card.metadata["composition_out"]

        if((composition_in_set =={"unknown"} or composition_in_set.issubset(composition_of_json)) and (composition_out_set =={"unknown"} or not bool(composition_out_set.intersection(composition_of_json)))):
            return True
        return False

class BlackWhiteMatcher(IMetadataMatcher):
    def is_match(self, json_elem, metadata_card):
        """
        return True if metadata_card and json_elem match on back/ white
        """
        if "contains_black" not in json_elem  or json_elem["contains_black"]=="" or json_elem["contains_black"]=="unknown":
            if "contains_white" not in json_elem  or json_elem["contains_white"]=="" or json_elem["contains_white"]=="unknown":
                return True
            
        if(metadata_card.metadata["contains_black"] == json_elem["contains_black"] or json_elem["contains_black"]=="unknown" or metadata_card.metadata["contains_black"]=="unknown") and (metadata_card.metadata["contains_white"] == json_elem["contains_white"] or json_elem["contains_white"] =="unknown" or metadata_card.metadata["contains_white"] == "unknown" ):
            return True
        if(metadata_card.metadata["contains_black"] == "unknown" and metadata_card.metadata["contains_white"] == "unknown"):
            return True
        
        return False
    
class OtherColorMatcher(IMetadataMatcher):
    def is_match(self, json_elem, metadata_card):
        """
        return True if metadata_card and json_elem match on contains_other_color
        """
        if "contains_other_color" not in json_elem  or json_elem["contains_other_color"]=="" or json_elem["contains_other_color"]=="unknown":
            return True
            
        if(metadata_card.metadata["contains_other_color"] == json_elem["contains_other_color"] or metadata_card.metadata["contains_other_color"] == "unknown"):
            return True
        
        return False

class GenreMatcher(IMetadataMatcher):
    def is_match(self, json_elem, metadata_card):
        """
        return True if metadata_card and json_elem match on genre
        """
        if "genre" not in json_elem  or json_elem["genre"]=="" or json_elem["genre"]=="unknown":
            return True
            
        if(metadata_card.metadata["genre"] == json_elem["genre"] or metadata_card.metadata["genre"] == "unknown"):
            return True
        
        return False

