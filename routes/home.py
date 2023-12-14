from flask import Flask, render_template, Blueprint

home = Blueprint('home', __name__)

views = ['bar_graph.html', 'line_graph.html','pie_chart.html','radar_chart.html','donut_chart.html',]
@home.route('/home')
def home_view():
    return render_template('home.html',data=views[0])

@home.route('/change_graph_view/<view>')
def change_graph_view(view):
    return render_template('home.html', data=views[int(view)])

