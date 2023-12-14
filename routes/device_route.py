from flask import Flask, render_template, Blueprint, url_for, redirect, request, jsonify, session

from db.connections import DatabaseConnection

device = Blueprint('device', __name__)


@device.route('/device')
def device_view():
    if 'customerID' in session:
        customerID = str(session['customerID'])
        address = fetch_service_address_by_customer_id(customerID)
        return render_template('device_view.html',  name = session['customerName'], dropDownList=fetch_all_device(), service_address = address, devices = fetch_device_by_id(customerID))
    return redirect(url_for('login.login_view'))

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
    return redirect(url_for('device.device_view'))


@device.route('/device/add', methods=['POST'])
def add_device():
    if request.method == 'POST':
        try:
            data = request.get_json()
            device_type = data.get('deviceType')
            device_model = data.get('deviceModel')
            sa_id = data.get('sa_id')
            conn = DatabaseConnection().connect()
            cursor = conn.cursor()
            cursor.execute('''
                                               SELECT MAX(deviceID) from Device;
                                                ''')
            deviceID = cursor.fetchall()[0][0] + 1
            #
            cursor.execute('''
                                   SELECT MAX(enrolledID) from Enrolled_Devices;
                                    ''')
            enrollID = cursor.fetchall()[0][0] + 1

            cursor.execute('''
                            INSERT INTO Device values(%s,%s,%s)
                           ''', (deviceID, device_type, device_model))

            cursor.execute('''
                                INSERT INTO Enrolled_Devices values(%s,%s,%s)
                               ''', (enrollID, sa_id, deviceID))
            conn.commit()
            DatabaseConnection().terminate()
            return jsonify(result=True)
        except Exception as e:
            print(e)
            return jsonify(result=False)
