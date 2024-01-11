import smtplib
from flask import Flask, render_template, request, flash, redirect,url_for
import json
import random
import machineLearningClassifier as mlc
import pandas as pd
app = Flask(__name__)



file_path = 'employee_db.txt'
file_path_transaction_status_from_to = 'transactionsStatus.txt'

csv_file_path = "final_dataset.csv"

@app.route('/')
def home_page_login():
    return render_template('user_login.html')




def sendMail(to_mail,otp):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("sanket.patil21@vit.edu", "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
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

        with open(file_path_transaction_status_from_to, 'r') as file:
            case_from_to_dict = json.load(file)
        no_of_cases = len(case_from_to_dict)
        no_of_cases_list = list(case_from_to_dict.keys())
        no_of_fradulent_records = 0
        no_of_suspicious_records = 0
        status_list=[]
        from_list=[]
        to_list=[]

        for i in no_of_cases_list:
            status_list.append(case_from_to_dict[i]["Status"])
            from_list.append(case_from_to_dict[i]["From"])
            to_list.append(case_from_to_dict[i]["To"])
            if case_from_to_dict[i]["Status"] == "Fradulent":
                no_of_fradulent_records += 1
            else:
                no_of_suspicious_records += 1

        combine_list = list(zip(no_of_cases_list, from_list, to_list,status_list))

        with open("case_employee.txt", 'r') as file:
            emp_cases = json.load(file)

        emp_cases_count = 0
        if emp_cases.get(mailID) is not None:
            emp_cases_count = len(list(emp_cases[mailID]))

        return render_template('employee_dashboard.html', text=person_name, no_of_cases=no_of_cases, no_of_fradulent_records=no_of_fradulent_records, no_of_suspicious_records=no_of_suspicious_records, emp_cases_count=emp_cases_count, combine_list=combine_list)
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



@app.route("/perform_analysis", methods=['POST'])
def perfom_analysis():
    my_obj = mlc.MachineLearningClassifier()
    status_lst = my_obj.transactionStatus()
    no_of_transactions = len(status_lst)
    no_of_valid_transactions = status_lst.count("Valid")
    no_of_fraudulent_transactions = status_lst.count("Fradulent")
    no_of_suspicious_transactions = status_lst.count("Suspicious")

    percentage_of_valid_transactions = (no_of_valid_transactions / no_of_transactions) * 100
    percentage_of_fraudulent_transactions = (no_of_fraudulent_transactions / no_of_transactions) * 100
    percentage_of_suspicious_transactions = (no_of_suspicious_transactions / no_of_transactions) * 100


    df = pd.read_csv(csv_file_path)
    columns_to_be_dropped = ['FraudIndicator', 'Category', 'AnomalyScore', 'Age', 'Address', 'AccountBalance', 'LastLogin', 'SuspiciousFlag']
    df = df.drop(columns_to_be_dropped, axis=1)
    df['Record Status'] = status_lst
    final_list = df.values.tolist()

    transaction_from_to_with_status = my_obj.returnTransactionIDWithStatusAndFromTo()
    keys_to_delete = [key for key,
                      value in transaction_from_to_with_status.items() if value["Status"] == "Valid"]

    for key in keys_to_delete:
        del transaction_from_to_with_status[key]

    with open(file_path_transaction_status_from_to, 'r') as file:
        loaded_dict = json.load(file)
    
    keys_list = list(transaction_from_to_with_status.keys())

    for i in keys_list:
        if i in loaded_dict.keys():
            print("Transaction already exists")
        else:
            loaded_dict[i] = transaction_from_to_with_status[i]



    with open(file_path_transaction_status_from_to, 'w') as convert_file:
        convert_file.write(json.dumps(loaded_dict))

    return render_template('admin_dashboard.html', total_records=no_of_transactions, valid_records=no_of_valid_transactions, fradulent_records=no_of_fraudulent_transactions, suspicious_records=no_of_suspicious_transactions, valid_records_percentage=str(percentage_of_valid_transactions)+"%", fradulent_records_percentage=str(percentage_of_fraudulent_transactions)+"%", suspicious_records_percentage=str(percentage_of_suspicious_transactions)+"%", temp_list=final_list)






@app.route("/validate_admin", methods=['POST'])
def validateAdmin():
    total_records = 0
    valid_records = 0
    fradulent_records = 0
    suspicious_records = 0

    valid_records_percentage = 0
    fradulent_records_percentage = 0
    suspicious_records_percentage = 0

    temp_list=[]

    status ="Invalid Password"
    password = request.form['password']
    if password == "admin":
        return render_template('admin_dashboard.html', total_records = total_records, valid_records = valid_records, fradulent_records = fradulent_records, suspicious_records = suspicious_records, valid_records_percentage=str(valid_records_percentage)+"%", fradulent_records_percentage = str(fradulent_records_percentage)+"%", suspicious_records_percentage = str(suspicious_records_percentage)+"%" ,temp_list=temp_list)
    else:
        return render_template('admin_login.html',status=status)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
