import json
class Encryptor:

    @staticmethod
    def xor_encryption(text):
        key = "a5555555ghfkglkdm"
        encrypted_text = ""
        for i in range(len(text)):
            encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))

        return encrypted_text


a =Encryptor.xor_encryption("{aaaaaabc: 5}")
print(a)
# data = json.loads(a)
# b = Encryptor.xor_encryption(data)
print(Encryptor.xor_encryption(a))



# print(data)
# print(type(data))
#
#
# {"machine": "data"}