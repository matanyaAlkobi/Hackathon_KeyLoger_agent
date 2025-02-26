from abc import ABC, abstractmethod

class IWriter(ABC):
    @staticmethod
    @abstractmethod
    def write(data):
        pass