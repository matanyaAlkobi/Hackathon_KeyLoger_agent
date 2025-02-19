from abc import ABC, abstractmethod

class IEncryptor(ABC):
    @abstractmethod
    def encryption(self,text, key: str):
        pass
    @abstractmethod
    def decryption(self,text, key: str):
        pass