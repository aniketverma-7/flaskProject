from flask import Flask, render_template, Blueprint, request, jsonify
from psycopg2 import IntegrityError

from db.connections import DatabaseConnection
from misc.password_encryption import encrypt

register = Blueprint('register', __name__)


@register.route('/register')
def register_view():  # put application's code here
    return render_template('register.html')

@register.route('/register/user', methods=['GET', 'POST'])
def add_user():
   if request.method == 'POST':
        try:
            if request.method == 'POST':
                data = request.get_json()
                name = data.get('name')
                email = data.get('email')
                password = data.get('password')
                baddress = data.get('baddress')
                conn = DatabaseConnection().connect()
                c = conn.cursor()
                c.execute("SELECT MAX(customerID) FROM customer")
                customerID = c.fetchall()[0][0] + 1
                c.execute('''INSERT INTO CUSTOMER VALUES (%s, %s, %s, %s, %s)''',
                          (customerID,name, email, encrypt(password), baddress))
                conn.commit()
                DatabaseConnection().terminate()
                return jsonify(result=True)
        except Exception as e:
            print(e)
            if 'unique_email' in str(e).lower():
                error ='Email address already in use'
            else:
                error = 'Server Error'
            return jsonify(result=False,error=error)

