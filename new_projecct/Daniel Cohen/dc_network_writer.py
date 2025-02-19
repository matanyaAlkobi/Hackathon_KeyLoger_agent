from IWriter import IWriter
import requests
import json


class Network_writer(IWriter):
    @staticmethod
    def write(data):

        SERVER_URL = "http://127.0.0.1:5000/upload"  # עדכן את כתובת השרת שלך
        try:
            response = requests.post(SERVER_URL, json=data)
            if response.status_code == 200:
                print("✅ הנתונים נשלחו בהצלחה!")
            else:
                print(f"⚠ שגיאה בשליחת הנתונים! קוד תגובה: {response.status_code}, תגובה: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ כשל בשליחת הנתונים: {e}")








import socket
print(socket.gethostbyname(socket.gethostname()))