from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home_page_login():
    return render_template('login.html')


@app.route("/admin_login", methods=['POST'])
def admin_login():
    return render_template('register.html')


@app.route("/register_user", methods=['POST'])
def register_user():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
