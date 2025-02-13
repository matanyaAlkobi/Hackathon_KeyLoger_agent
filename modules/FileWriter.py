import json
from IWriter import *

class FileWriter(IWriter):

    def write(self, data):
        with open(r"C:\Users\matan\kodkod\programming\Hackathon_KeyLoger_agent\new_projecct\matanya alkobi\output\new.json" , "a" , encoding="utf-8") as file:
            if data:
                json.dump(data , file ,ensure_ascii=False,  indent=4)