from flask import Flask, render_template, Blueprint, request, jsonify, session, redirect, url_for

from db.connections import DatabaseConnection
from misc.password_encryption import checkPassword

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
        c.execute("SELECT CustomerID, Cemail, Cpassword FROM customer WHERE LOWER(Cemail) = %s", (username,))

        customerID, storedUser, storedPassword = c.fetchall()[0]
        print(customerID)
        # result=""
        if not checkPassword(password, storedPassword):
            result = ""
        else:
            result = "Success"
            # print(session['customerID'])
            session['customerID'] = request.form[customerID]
            return redirect(url_for('home.home_view'), 200)

        print(result)
        # # Return a JSON response
        return jsonify(result=result)
        # print(username, password)
        # return True
    return True

# def sessionValidate
