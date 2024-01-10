class MetadataMatchingController:
    def __init__(self, matchers):
        self.matchers = matchers

    def meta_match(self, json_elem, metadata_card):
        """
        returns true if metadata_card matches json_elem
        """
        return all(matcher.is_match(json_elem, metadata_card) for matcher in self.matchers.values())
