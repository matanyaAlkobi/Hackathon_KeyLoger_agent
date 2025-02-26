from KeyloggerService import *
from IEncryptor import *
import json

class XOREncryptor(IEncryptor):
    def encryption(self,text, key: str):
        # המרת הטקסט למיתרים אם הוא לא כבר מיתרים
        text = json.dumps(text)  # המרת המילון למיתר JSON
        encrypted_text = []

        # ביצוע XOR בין כל תו בטקסט לבין המפתח
        for i in range(len(text)):
            # המרה של התו למספר ASCII ו-XOR עם התו במפתח
            encrypted_text.append(str(ord(text[i]) ^ ord(key[i % len(key)])))

        return encrypted_text

    def  decryption(self,encrypted_text, key: str):
        decrypted_text = ""

        # ביצוע XOR כדי להחזיר את הטקסט המקורי
        for i in range(len(encrypted_text)):
            # המרה של כל ערך לרשימה של מספרים
            encrypted_value = int(encrypted_text[i])  # המרת המיתר חזרה למספר
            decrypted_text += chr(encrypted_value ^ ord(key[i % len(key)]))  # XOR והמרה חזרה לתו

        # ניסוי להמיר את התוצאה לפורמט JSON
        return json.loads(decrypted_text)  # אם זה היה JSON תקני, נחזיר אותו


