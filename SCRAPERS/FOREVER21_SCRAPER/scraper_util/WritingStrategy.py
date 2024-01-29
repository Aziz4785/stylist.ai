from abc import ABC, abstractmethod

class WritingStrategy(ABC):
    """
    Abstract base class for DB writing strategies.
    """
    @abstractmethod
    def write(self, data):
        pass
