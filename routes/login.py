from flask import Flask, render_template, Blueprint, request, jsonify

from db.connections import DatabaseConnection
from misc.password_encryption import decrypt

login = Blueprint('login', __name__)


@login.route('/login')
def login_view():  # put application's code here
    return render_template('login.html')

@login.route('/login/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        # Handle the AJAX request
        data = request.get_json()
        username = str(data.get('email')).lower()
        password = data.get('password')
        conn = DatabaseConnection()
        c = conn.connect().cursor()
        c.execute("SELECT Cemail, Cpassword FROM customer WHERE Cemail = %s", (username, ))

        storeUser, storePassword = c.fetchall()[0]
        result=""
        if not decrypt(password,storePassword):
            result = "Invalid Password"
        else:
            result = "Success"
        print(result)
        # Return a JSON response
        return jsonify(result=result)
        print(username, password)
    return True

# def sessionValidate