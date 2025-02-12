import json


class FileWriter:
    @staticmethod
    def write_to_file(data:dict):
        with open(r"C:\Users\matan\kodkod\programming\Hackathon_KeyLoger_agent\new_projecct\matanya alkobi\output\my.json" , "w" , encoding="utf-8") as file:
            json.dump(data , file ,ensure_ascii=False)
