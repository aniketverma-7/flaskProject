from flask import Flask, render_template, Blueprint, session, redirect, url_for

from db.connections import DatabaseConnection

home = Blueprint('home', __name__)

views = ['bar_graph.html', 'line_graph.html','pie_chart.html','radar_chart.html','donut_chart.html',]
@home.route('/home')
def home_view():
    if 'customerID' in session:
        keys, values = get_data(str(session['customerID']), "2")
        labels = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
        label = 'Weekly Energy Consumption'
        if type == "2":
            labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                      "November", "`December"]
            label = 'Monthly Energy Consumption'
        if type == "3":
            labels = keys
            label = 'Yearly Energy Consumption'
        return render_template('home.html', file=views[0], values=values, label=label, labels=labels, name = session['customerName'])

    return redirect(url_for('login.login_view'))

@home.route('/change_graph_view/<view>/<type>/')
def change_graph_view(view, type):
    print(view,type)
    keys, values = get_data(str(session['customerID']), type)
    labels = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    label = 'Weekly Energy Consumption'
    if type == "2":
        labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "`December"]
        label = 'Monthly Energy Consumption'
    if type == "3":
        labels = keys
        label = 'Yearly Energy Consumption'
    return render_template('home.html', file=views[int(view)], values=values, label=label, labels=labels, name = session['customerName'])

def get_data(customerID, type):
    cursor = DatabaseConnection().connect().cursor()
    type_s = "DOW"
    if type == "2":
        type_s = "MONTH"
    if type == "3":
        type_s = "YEAR"
    cursor.execute(f"""
                SELECT EXTRACT({type_s} FROM CAST(B.EP_Timestamp AS DATE)) AS bucket,
                SUM(CAST(A.DD_Value AS float) * CAST(B.Hourly_Price AS float)) AS cost
                FROM (SELECT DD.DD_Value, DD.DD_TimeStamp FROM
                    (SELECT DeviceID FROM (
                        SELECT SA_ID FROM Service_Address Where CustomerID = %s
                        ) SA JOIN Enrolled_Devices ED ON SA.SA_ID = ED.SA_ID
                    ) SA_ED JOIN DeviceData DD ON SA_ED.DeviceID = DD.DeviceID
                ) A JOIN Energy_Price B ON EXTRACT(
                    {type_s} FROM CAST(A.DD_TimeStamp AS DATE)) = EXTRACT(
                    {type_s} FROM CAST(B.EP_Timestamp AS DATE))
                GROUP BY 1
                """, (customerID))
    data = cursor.fetchall()
    key_dict = [int(key) for key, value in data]
    value_dict = [int(value) for key, value in data]
    return key_dict, value_dict