from flask import Blueprint, request, flash, redirect, url_for

bp = Blueprint('search', __name__)

@bp.route('/', methods=['POST'])
def search():
    return redirect(url_for('index.index', country=request.form['country']))