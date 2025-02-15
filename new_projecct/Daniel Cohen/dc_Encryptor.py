class Encryptor:
    @staticmethod
    def xor_encryption(text):
        key = "a"
        encrypted_text = ""
        for i in range(len(text)):
            encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))
        return encrypted_text