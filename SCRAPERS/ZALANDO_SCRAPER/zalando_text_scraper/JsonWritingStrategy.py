from abc import ABC, abstractmethod

class JsonWritingStrategy(ABC):
    """
    Abstract base class for JSON writing strategies.
    """
    @abstractmethod
    def write_json(self, data):
        pass
