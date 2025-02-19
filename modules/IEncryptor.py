from abc import ABC, abstractmethod

class IEncryptor(ABC):
    @abstractmethod
    def encryption(self,text):
        pass
    @abstractmethod
    def decryption(self,text):
        pass