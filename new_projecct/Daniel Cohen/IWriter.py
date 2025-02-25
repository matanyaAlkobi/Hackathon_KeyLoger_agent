# from abc import ABC, abstractmethod
#
# class IWriter(ABC):
#     @staticmethod
#     @abstractmethod
#     def write(data):
#         pass


import json

def get_first_string_from_json(json_content):
    """
    מקבלת מחרוזת JSON ומחזירה את הסטרינג הראשון שנמצא בתוכה.
    בדוגמה של JSON כמו {"abc":123} – תוחזר המחרוזת "abc".

    :param json_content: מחרוזת בפורמט JSON
    :return: הסטרינג הראשון או None אם לא נמצא
    """
    try:
        data = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"תקלה בפירוש JSON: {e}")
        return None

    # אם מדובר במילון, נניח שהסדר נשמר ונשלוף את המפתח הראשון.
    if isinstance(data, dict):
        for key in data.keys():
            if isinstance(key, str):
                return key
        return None  # אם אין מפתחות שהם מחרוזות

    # אם מדובר במבנה אחר (למשל, רשימה) ננסה למצוא את הסטרינג הראשון
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                return item
        return None

    else:
        # במקרה של טיפוס אחר, נבדוק אם עצמו הוא מחרוזת
        if isinstance(data, str):
            return data
        return None

# דוגמה לשימוש:
json_str = '{"abc":123}'
first_string = get_first_string_from_json(json_str)
print(f"הסטרינג הראשון ב-JSON הוא: {first_string}")