from flask import Blueprint, redirect, request, url_for

from package.models.product import Product

bp = Blueprint('result', __name__)

@bp.route('/', methods=['GET'])
def result():
    cookie = request.cookies.get('uid')
    if cookie is not None:
        with open(f'{cookie}.csv', 'r') as f:
            rl = f.readlines()
            for i in rl:
                i = i.split()
                i = [*i[:-1], i[-1][:-1]]
                # calculations
    else:
        return redirect(url_for('index.index'))
