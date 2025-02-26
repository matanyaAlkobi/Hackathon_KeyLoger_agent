import json

class FileWriter:
    @staticmethod
    def write_to_file(data:dict):
        print("aaaq")
        if data :
            with open(r"C:\Users\1\projet keylogger kodkode\keys.json" , "w" , encoding="utf-8") as file:
                json.dump(data , file ,ensure_ascii=False , indent=4)

        #     for
        # print("3 secends")