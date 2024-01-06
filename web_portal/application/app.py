from flask import Flask, render_template, request, flash, redirect,url_for
import json
app = Flask(__name__)



@app.route('/')
def home_page_login():
    return render_template('login.html')


@app.route("/admin_login", methods=['POST'])
def admin_login():
    return render_template('admin_login.html')


@app.route("/add_employee", methods=['POST'])
def addEmployee():
    return render_template('employers_registration.html')
    # redirect(url_for('user_login.html'))


@app.route("/back_to_admin_dashboard", methods=['POST'])
def backToAdminDashboard():
    return render_template('admin_dashboard.html')


@app.route("/register_user", methods=['POST'])
def registerUser():
    success_status = "Employee Successfully added"
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']

    file_path = 'employee_db.txt'
    with open(file_path, 'r') as file:
        loaded_dict = json.load(file)

    if email in loaded_dict.keys():
        success_status = "Employee already exists."
        pass
    else:
        loaded_dict[email] = {"fname": fname, "lname":lname}
    with open(file_path, 'w') as convert_file:
        convert_file.write(json.dumps(loaded_dict))
    return render_template('employers_registration.html',status = success_status)




@app.route("/validate_admin", methods=['POST'])
def validateAdmin():
    status ="Invalid Password"
    password = request.form['password']
    if password == "admin":
        return render_template('admin_dashboard.html')
    else:
        return render_template('admin_login.html',status=status)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
