from flask import Flask, render_template, Blueprint, request, jsonify

from db.connections import DatabaseConnection
from misc.password_encryption import decrypt

register = Blueprint('register', __name__)


@register.route('/register')
def register_view():  # put application's code here
    return render_template('register.html')

@register.route('/register/user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Handle the AJAX request
        data = request.get_json()
        username = str(data.get('userID')).lower()
        password = data.get('password')
        conn = DatabaseConnection()
        c = conn.connect().cursor()
        c.execute("SELECT Cemail, Cpassword FROM customer WHERE Cemail = %s", (username,))
    return True


