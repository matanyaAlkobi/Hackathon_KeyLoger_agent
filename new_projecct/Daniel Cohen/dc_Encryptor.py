
import json

class Encryptor:

    @staticmethod
    def xor_encryption(text, key: str):
        # המרת הטקסט למיתרים אם הוא לא כבר מיתרים
        text = json.dumps(text)  # המרת המילון למיתר JSON
        encrypted_text = []

        # ביצוע XOR בין כל תו בטקסט לבין המפתח
        for i in range(len(text)):
            # המרה של התו למספר ASCII ו-XOR עם התו במפתח
            encrypted_text.append(str(ord(text[i]) ^ ord(key[i % len(key)])))

        return encrypted_text

    @staticmethod
    def xor_decryption(encrypted_text, key):
        decrypted_text = ""

        # ביצוע XOR כדי להחזיר את הטקסט המקורי
        for i in range(len(encrypted_text)):
            # המרה של כל ערך לרשימה של מספרים
            encrypted_value = int(encrypted_text[i])  # המרת המיתר חזרה למספר
            decrypted_text += chr(encrypted_value ^ ord(key[i % len(key)]))  # XOR והמרה חזרה לתו

        # ניסוי להמיר את התוצאה לפורמט JSON
        return json.loads(decrypted_text)  # אם זה היה JSON תקני, נחזיר אותו



# a = {"gsf": {"123": {"987":657}}}  # מילון
# b = Encryptor.xor_encryption(a, "aaa")  # הצפנה עם XOR
# b = json.dumps(b)
# print(b)  # צפוי להחזיר רשימה של מספרים
# print(type(b))
# b = json.loads(b)# רשימה של מיתרים
# print(type(b))
# print("rrrr")
# c = Encryptor.xor_decryption(b, "aaa")  # פענוח עם XOR
# print(c)  # צפוי להחזיר את המילון המקורי
# print(type(c))  # צפוי להחזיר dict או str (תלוי בתוצאה)
