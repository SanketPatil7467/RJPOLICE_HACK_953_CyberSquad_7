import smtplib
from flask import Flask, render_template, request, flash, redirect,url_for
import json
import random
app = Flask(__name__)



file_path = 'employee_db.txt'

@app.route('/')
def home_page_login():
    return render_template('user_login.html')




def sendMail(to_mail,otp):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("sanket.patil21@vit.edu", "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    message = f"Hello your otp is {otp}"
    s.sendmail("sanket.patil21@vit.edu", to_mail, message)
    s.quit()


@app.route("/request_otp", methods=['POST'])
def request_otp():
    global mailID
    usr_mail = request.form['mail_text']
    mailID = usr_mail
    successful_str = f"OTP sent to {usr_mail}"
    invalid_mail = f"{usr_mail} not exists"
    global otp;

    
    with open(file_path, 'r') as file:
        loaded_dict = json.load(file)
    
    if usr_mail in loaded_dict.keys():
        otp = random.randint(1000,9999)
        sendMail(usr_mail,str(otp))
        return render_template('user_login.html', text=successful_str)

        
    else:
        return render_template('user_login.html',text=invalid_mail)


@app.route("/validate_otp", methods=['POST'])
def validate_otp():
    usr_otp = request.form['otp_text']
    print(mailID)
    print(type(mailID))

    if usr_otp == str(otp):
        with open(file_path, 'r') as file:
            loaded_dict = json.load(file)
        person_name = loaded_dict[mailID]["fname"] + " " + loaded_dict[mailID]["lname"]
        print(person_name)
        return render_template('employee_dashboard.html', text=person_name)
    else:
        return render_template('user_login.html', text2="Invalid OTP")





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
