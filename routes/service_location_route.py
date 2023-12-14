from flask import Flask, render_template, Blueprint, request, jsonify, session, redirect, url_for

from db.connections import DatabaseConnection

service_location = Blueprint('service_location', __name__)


@service_location.route('/service-location')
def service_location_view():
    if 'customerID' in session:
        customerID = session['customerID']
        return render_template('service_location_view.html', name=session['customerName'],
                               service_locations=fetch_service_address(customerID))
    return redirect(url_for('login.login_view'))


def fetch_service_address(customerID):
    cursor = DatabaseConnection().connect().cursor()
    cursor.execute('''SELECT DISTINCT *
                        FROM Service_Address
                        WHERE customerID = %s'''
                   , (customerID,))
    service_address = cursor.fetchall()
    return service_address


@service_location.route('/service-address/add', methods=['GET', 'POST'])
def add_service_address():
    if request.method == 'POST':
        try:
            data = request.get_json()
            customerID = session['customerID']
            apartmentNumber = data.get('apartmentNumber')
            block = data.get('blockNumber')
            street = data.get('streetName')
            city = data.get('city')
            state = data.get('state')
            zipcode = data.get('zipCode')
            squareFoot = data.get('squareFoot')
            occupants = data.get('occupants')
            bedrooms = data.get('bedrooms')
            moveInDate = data.get('moveInDate')
            conn = DatabaseConnection().connect()
            cursor = conn.cursor()
            cursor.execute('''
                                         SELECT MAX(SA_ID) from Service_Address;
                                          ''')
            sa_id = cursor.fetchall()[0][0] + 1
            query = "INSERT INTO Service_Address (SA_ID, CustomerID, Unit, Block, Street, Occupants, Bedrooms, Zipcode, Square_foot, Move_in_date, City, SA_State) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (sa_id,
                                   customerID, apartmentNumber, block, street, occupants, bedrooms, zipcode,
                                   squareFoot, moveInDate, city, state
                                   ))
            conn.commit()
            DatabaseConnection().terminate()
            return jsonify(result=True)
        except Exception as e:
            print(e)
            return jsonify(result=False)


@service_location.route('/service-location/delete', methods=['POST'])
def delete_service_address_by_id():
    if request.method == 'POST':
        try:
            data = request.get_json()
            sa_id = str(data.get('sa_id'))
            conn = DatabaseConnection().connect()
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM ENROLLED_DEVICES WHERE SA_ID = %s;
                                            ''', (sa_id,))
            cursor.execute('''
                               DELETE FROM SERVICE_ADDRESS WHERE SA_ID = %s;
                                ''', (sa_id,))
            conn.commit()
            DatabaseConnection().terminate()
            return jsonify(result=True)
        except Exception as e:
            print(e)
            return jsonify(result=False)
