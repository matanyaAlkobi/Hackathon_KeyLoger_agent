from abc import ABC, abstractmethod
from FileWriter import *

class IWriter(ABC):
    @abstractmethod
    def write(self, data):
        pass