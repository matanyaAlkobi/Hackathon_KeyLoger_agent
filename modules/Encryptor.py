from KeyloggerService import *
from modules.IEncryptor import *
import json

class XOREncryptor(IEncryptor):
    def encryption(self,text, key: str):

        text = str(text)
        encrypted_text = []

        for i in range(len(text)):
            encrypted_text.append(ord(text[i]) ^ ord(key[i % len(key)]))

        return encrypted_text

    def  decryption(self,encrypted_text, key: str):

        decrypted_text = ""

        for i in range(len(encrypted_text)):
            decrypted_text += chr(encrypted_text[i] ^ ord(key[i % len(key)]))

        return json.loads(decrypted_text.replace("'", '"'))






