from flask import Flask, render_template, request, flash
import json
app = Flask(__name__)



@app.route('/')
def home_page_login():
    return render_template('login.html')


@app.route("/admin_login", methods=['POST'])
def admin_login():
    return render_template('register.html')


@app.route("/register_user", methods=['POST'])
def register_user():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']

    if password == "admin":
        file_path = 'employee_db.txt'
        with open(file_path, 'r') as file:
            loaded_dict = json.load(file)

        if email in loaded_dict.keys():
            # Employee already exists
            pass
        else:
            loaded_dict[email] = {"fname": fname, "lname":lname}
        with open(file_path, 'w') as convert_file:
            convert_file.write(json.dumps(loaded_dict))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
