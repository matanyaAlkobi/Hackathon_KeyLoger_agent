import json

class Encryption:

    @staticmethod
    def xor_encryption(text ,key: str):
        text = str(text)
        encrypted_text = []

        for i in range(len(text)):
            encrypted_text.append(ord(text[i]) ^ ord(key[i % len(key)]))

        return encrypted_text

    @staticmethod
    def xor_decryption(encrypted_text,key):
        decrypted_text = ""

        for i in range(len(encrypted_text)):
            decrypted_text += chr(encrypted_text[i] ^ ord(key[i % len(key)]))

        return json.loads(decrypted_text)

s = {"trsd}tgvsr":"ttttt"}

data = json.dumps(s)
print(type(data))

b = Encryption()
# enc =b.xor_decryption(data,"a")
# print(type(enc))
enc = Encryption.xor_encryption(data,"a")
print(enc)
dec = Encryption.xor_decryption(enc,"a")
print(dec)
# new = json.loads(dec)
print(type(dec))
# print(new['trsdtgvsr'])





