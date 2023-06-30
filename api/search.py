from flask import Blueprint, request, flash, redirect, url_for

from api.main import db
from api.models.input import Input

bp = Blueprint('search', __name__)

@bp.route('/', methods=['POST'])
def search():
    country, name, quantity, time = request.form['country'], request.form['name'], request.form['quantity'], request.form['time_used']
    cookie = request.cookies.get('uid')
    details = Input(cookie=cookie, type_device=True, device_country=country, device_name=name, device_quantity=quantity, device_time=time)
    db.session.add(details)
    db.session.commit()
    return redirect(url_for('index.index', country=request.form['country']))

@bp.route('/flight', methods=['POST'])
def flight():
    origin, destination, airline, flight_no, date, flight_class = request.form['origin'], request.form['destination'], request.form['airline'], request.form['flight'], request.form['date'], request.form['class']
    cookie = request.cookies.get('uid')
    details = Input(cookie=cookie, type_device=False, flight_origin=origin, flight_destination=destination, flight_airline=airline, flight_number=flight_no, flight_date=date, flight_class=flight_class)
    db.session.add(details)
    db.session.commit()
    return redirect(url_for('index.index'))