import os

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for

from routes.device_route import device
from routes.home import home
from routes.login import login
from routes.register import register
from routes.service_location_route import service_location

# from routes import login
app = Flask(__name__)
app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(home)
app.register_blueprint(device)
app.register_blueprint(service_location)

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def start():  # put application's code here
    return redirect(url_for('login.login_view'))


if __name__ == '__main__':
    app.run()
