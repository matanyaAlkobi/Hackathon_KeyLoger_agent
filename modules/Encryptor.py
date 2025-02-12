class Encryptor:

    def xor_encryption(self,text, key):
        # Initialize an empty string for encrypted text
        encrypted_text = ""

        # Iterate over each character in the text
        for i in range(len(text)):
            encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))

        # Return the encrypted text
        return encrypted_text

a = Encryptor()
b= a.xor_encryption("matan","h")
c=a.xor_encryption(b,"h")
print(b)
print(c)
