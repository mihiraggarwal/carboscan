import os
import matplotlib.pyplot as plt
import subprocess
from flask import Blueprint, make_response, redirect, render_template, request, url_for

from package.models.product import Product

bp = Blueprint('result', __name__)


def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass
runcmd("wget -P /tmp https://raw.githubusercontent.com/h4pZ/rose-pine-matplotlib/main/themes/rose-pine.mplstyle")

def create_subplots():
    data = {'apple': 10, 'orange': 15, 'lemon': 5, 'lime': 20}
    names = list(data.keys())
    values = list(data.values())

    fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
    axs[0].bar(names, values)
    axs[1].scatter(names, values)
    axs[2].plot(names, values)
    fig.suptitle('Categorical Plotting')

    # path exists
    if os.path.exists("package/static/chart.png"):
        os.remove("package/static/chart.png")
        plt.savefig("package/static/chart.png")
    else:
        plt.savefig("package/static/chart.png")

with plt.style.context("/tmp/rose-pine.mplstyle"):
    create_subplots()


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
