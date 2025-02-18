class IEncrypter(ABC):
    @abstractmethod
    def encrypt(self,text):
        pass

    @abstractmethod
    def decrypt(self,encrypted_text):
        pass

class XOREncryption(IEncrypter):

    def _init_(self,password):
        self.__password = password


    def encrypt(self,text):
        """
        Accepts unencrypted text and encrypts
         it using the XOR method
        :param text: unencrypted text
        :return: encrypted text
        """
        xor_encrypted = list(
            (ord(x) ^ ord(y))
            for x, y in zip(
                text, self._password * (len(text) // len(self.password)) + self.password[: len(text) % len(self._password)]
            )
        )
        return xor_encrypted

    # Decode using XOR
    def decrypt(self,encrypted_text):
        """
        Receives an encrypted text using the XOR method and
         returns the unencrypted (original) text
        :param encrypted_text: encrypted text
        :return: unencrypted text
        """
        return ''.join(
            chr(x ^ ord(y))
            for x, y in zip(
                encrypted_text,
                self._password * (len(encrypted_text) // len(self._password))
                + self._password[: len(encrypted_text) % len(self._password)]
            )
        )