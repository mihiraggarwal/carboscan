from flask import Blueprint, request, flash, redirect, url_for

bp = Blueprint('search', __name__)

@bp.route('/', methods=['POST'])
def search():
    data = f"{request.form['country']},{request.form['name']},{request.form['quantity']},{request.form['time_used']}\n"
    cookie = request.cookies.get('uid')
    with open(f'{cookie}.csv', 'a') as f:
        f.write(data)
    return redirect(url_for('index.index', country=request.form['country']))

@bp.route('/flight', methods=['POST'])
def flight():
    data = f"{request.form['origin']},{request.form['destination']},{request.form['airline']},{request.form['flight']},{request.form['date']},{request.form['class']}\n"
    cookie = request.cookies.get('uid')
    with open(f'{cookie}-flight.csv', 'a') as f:
        f.write(data)
    return redirect(url_for('index.index'))