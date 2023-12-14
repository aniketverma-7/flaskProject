from flask import Flask, render_template, Blueprint

from db.connections import DatabaseConnection
from models.device import Device

device = Blueprint('device', __name__)


@device.route('/device/<customerID>')
def device_view(customerID):
    return render_template('device_view.html', devices = fetch_device(customerID))


def fetch_device(customerID):
    cursor = DatabaseConnection().connect().cursor()
    cursor.execute('''SELECT DISTINCT d.*
                        FROM Customer c
                        JOIN Service_Address sa ON c.CustomerID = sa.CustomerID
                        JOIN Enrolled_Devices ed ON sa.SA_ID = ed.SA_ID
                        JOIN Device d ON d.deviceID = ed.deviceID
                        WHERE c.CustomerID = %s
                        ORDER BY deviceid ASC;'''
                   , (customerID,))
    devices = cursor.fetchall()
    return devices

