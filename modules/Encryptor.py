from KeyloggerService import *

def xor_enryption(text, key):
    # Initialize an empty string for encrypted text
    encrypted_text = ""

    # Iterate over each character in the text
    for i in range(len(text)):
        encrypted_text += str(ord(text[i]) ^ ord(key[i % len(key)]))

    # Return the encrypted text
    return encrypted_text

a = xor_enryption("matan","hello")
print(a)
a = xor_enryption(a,"hello")
print(a)


