import os
from flask import Blueprint, make_response, redirect, render_template, request, url_for

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
        resp = make_response(render_template('result.html'))
        resp.set_cookie('uid', '', expires=0)
        os.remove(f'{cookie}.csv')
        return resp
    else:
        return redirect(url_for('index.index'))
