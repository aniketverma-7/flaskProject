from flask import Flask, render_template, Blueprint, request, jsonify

from db.connections import DatabaseConnection

service_location = Blueprint('service_location', __name__)


@service_location.route('/service-location/<customerID>')
def service_location_view(customerID):
    return render_template('service_location_view.html', service_locations=fetch_service_address(customerID))


def fetch_service_address(customerID):
    cursor = DatabaseConnection().connect().cursor()
    cursor.execute('''SELECT DISTINCT *
                        FROM Service_Address
                        WHERE customerID = %s'''
                   , (customerID,))
    service_address = cursor.fetchall()
    print(len(service_address))
    return service_address


@service_location.route('/service-address/add', methods=['GET','POST'])
def add_service_address():
    customerID = request.form.get('customerID')
    apartmentNumber = request.form.get('apartmentNumber')
    block = request.form.get('blockNumber')
    street = request.form.get('streetName')
    city = request.form.get('city')
    state = request.form.get('state')
    zipcode = request.form.get('zipCode')
    squareFoot = request.form.get('squareFoot')
    occupants = request.form.get('occupants')
    bedrooms = request.form.get('bedrooms')
    moveInDate = request.form.get('moveInDate')

    conn = DatabaseConnection().connect()
    cursor =conn.cursor()
    query = "INSERT INTO Service_Address (CustomerID, Unit, Block, Street, Occupants, Bedrooms, Zipcode, Square_foot, Move_in_date, City, SA_State) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (
        customerID, apartmentNumber, block, street, occupants, bedrooms, zipcode,
        squareFoot, moveInDate, city, state
    ))
    response_data = {'status': 'success', 'message': 'Form data received successfully'}
    return jsonify(response_data)

    # except Exception as e:
    # # Handle exceptions or validation errors
    # response_data = {'status': 'error', 'message': str(e)}
    # return jsonify(response_data), 400  # Return 400 status code for bad request


