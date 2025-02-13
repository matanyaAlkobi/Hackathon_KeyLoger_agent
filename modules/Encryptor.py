from KeyloggerService import *

def xor_encryption(text, key):
    # Initialize an empty string for encrypted text
    encrypted_text = ""

    # Iterate over each character in the text
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))

    # Return the encrypted text
    return encrypted_text

a = xor_encryption("matan","hello")
print(a)
a = xor_encryption(a,"hello")
print(a)


