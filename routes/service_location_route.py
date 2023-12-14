from flask import Flask, render_template, Blueprint

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


