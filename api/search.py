from flask import Blueprint, request, flash, redirect, url_for

bp = Blueprint('search', __name__)

@bp.route('/', methods=['POST'])
def search():
    data = f"{request.form['country']},{request.form['name']},{request.form['quantity']},{request.form['time_used']}\n"
    cookie = request.cookies.get('uid')
    with open(f'{cookie}.csv', 'a') as f:
        f.write(data)
    return redirect(url_for('index.index', country=request.form['country']))