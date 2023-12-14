from flask import Flask, render_template, Blueprint, url_for, redirect, request, jsonify

from db.connections import DatabaseConnection
from models.device import Device
from routes.service_location_route import fetch_service_address

device = Blueprint('device', __name__)


@device.route('/device/<customerID>')
def device_view(customerID):
    address = fetch_service_address_by_customer_id(customerID)
    return render_template('device_view.html', dropDownList=fetch_all_device(), service_address = address, devices = fetch_device_by_id(customerID))


def fetch_all_device():
    cursor = DatabaseConnection().connect().cursor()
    cursor.execute('''SELECT DISTINCT * FROM Device;''')
    devices = cursor.fetchall()
    DatabaseConnection().terminate()
    return devices

def fetch_service_address_by_customer_id(customerID):
    cursor = DatabaseConnection().connect().cursor()
    cursor.execute('''SELECT DISTINCT * FROM Service_Address where customerId = %s;''', customerID)
    address = cursor.fetchall()
    f_address = []
    for i in address:
        temp = str(i[2]) + " " + str(i[3]) + " " + str(i[4]) + " " + str(i[10]) + " " + str(i[11])
        f_address.append([i[0], temp])
        print(temp)
    DatabaseConnection().terminate()
    return f_address
def fetch_device_by_id(customerID):
    cursor = DatabaseConnection().connect().cursor()
    cursor.execute('''SELECT DISTINCT d.*, sa.sa_id, sa.unit, sa.block, sa.street, sa.city, sa.sa_state, sa.zipcode
                        FROM Customer c
                        JOIN Service_Address sa ON c.CustomerID = sa.CustomerID
                        JOIN Enrolled_Devices ed ON sa.SA_ID = ed.SA_ID
                        JOIN Device d ON d.deviceID = ed.deviceID
                        WHERE c.CustomerID = %s
                        ORDER BY deviceid ASC;'''
                   , (customerID,))
    devices = cursor.fetchall()
    DatabaseConnection().terminate()
    return devices

@device.route('/device/delete/<deviceID>/<sa_id>')
def deleteDevice(deviceID,sa_id):
    conn = DatabaseConnection().connect()
    cursor = conn.cursor()
    cursor.execute('''
                    DELETE FROM Enrolled_Devices
                    WHERE DeviceID = %s and SA_ID = %s;
                    ''', (deviceID, sa_id))
    conn.commit()
    DatabaseConnection().terminate()
    return redirect(url_for('device.device_view', customerID = 2))


@device.route('/device/add', methods=['POST'])
def add_device():
    device_type = request.form.get('deviceType')
    device_model = request.form.get('deviceModel')
    conn = DatabaseConnection().connect()
    cursor = conn.cursor()
    cursor.execute('''
                       SELECT MAX(DeviceId) from Device;
                        ''')
    m = cursor.fetchall()[0][0]
    # cursor.execute('''
    #                 INSERT INTO Device values(%s,%s,%s)
    #                ''', m+1, device_type, device_model)
    #
    # cursor.execute('''
    #                     INSERT INTO Device values(%s,%s,%s)
    #                    ''', m + 1, device_type, device_model)
    conn.commit()
    print(m)
    DatabaseConnection().terminate()
    return jsonify({'status': 'success', 'message': f'Device added: {device_type} - {device_model}'})
