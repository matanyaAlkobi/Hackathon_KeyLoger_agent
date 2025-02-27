# class Encryptor:

def xor_encryption(text, key):
    # Initialize an empty string for encrypted text
    encrypted_text = ""

    # Iterate over each character in the text
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))

    # Return the encrypted text
    return encrypted_text



print(xor_encryption("matan","hello"))


# a  = Encryptor()
# print(a.xor_encryption("matan","hello"))
# print(a.xor_encryption("mosh","hello"))