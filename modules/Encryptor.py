from KeyloggerService import *
from modules.IEncryptor import IEncryptor


class XOREncryptor(IEncryptor):
    def encryption(self,text):
        key = "hello"
        # Initialize an empty string for encrypted text
        encrypted_text = ""

        # Iterate over each character in the text
        for i in range(len(text)):
            encrypted_text += str(ord(text[i]) ^ ord(key[i % len(key)]))

        # Return the encrypted text
        return encrypted_text

    def  decryption(self,text):
        return self.encryption(text)


