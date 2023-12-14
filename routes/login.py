from flask import Flask, render_template, Blueprint, request, jsonify, session, redirect, url_for

from db.connections import DatabaseConnection
from misc.password_encryption import checkPassword

login = Blueprint('login', __name__)


@login.route('/login')
def login_view():  # put application's code here
    return render_template('login.html')


@login.route('/login/auth', methods=['GET', 'POST'])
def auth():
    print("Authenticating................")
    if request.method == 'POST':
        # Handle the AJAX request
        try:
            data = request.get_json()
            username = str(data.get('email')).lower()
            password = data.get('password')
            conn = DatabaseConnection()
            c = conn.connect().cursor()
            c.execute("SELECT CustomerID, CName, Cemail, Cpassword FROM customer WHERE LOWER(Cemail) = %s", (username,))
            customerID, customerName, storedUser, storedPassword = c.fetchall()[0]
            if not checkPassword(password, storedPassword):
                print("Authentication failed")
                raise "User not found"
            else:
                print( "Authentication Successful")
                session['customerName'] = customerName.split()[0]
                session['customerID'] = customerID
                return  jsonify(result=True)
        except Exception as e:
            return jsonify(result=False)

@login.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('customerID', None)
    session.pop('customerName', None)
    return redirect(url_for('login.login_view'))

