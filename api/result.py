import os
import os.path
from pathlib import Path
import matplotlib as mpl
import requests
import matplotlib.pyplot as plt
import subprocess
from flask import Blueprint, make_response, redirect, render_template, request, url_for
import sqlite3
import requests
from dotenv import load_dotenv

from api.models.product import Product

bp = Blueprint('result', __name__)
load_dotenv()

def dbsearch(id_list:list):
    # sqliteConnection = sqlite3.connect('../instance/$databasename')  # replace $databasename with file name
    # cursor = sqliteConnection.cursor()
    # print("Database created and Successfully Connected to SQLite")

    # sqlite_select_Query = "select * from devices where dev_id in {}".format(id_list)
    # cursor.execute(sqlite_select_Query)
    # # dev_id, deviceName, productEmission, powerRating, powerDuration
    # records = cursor.fetchall()
    # cursor.close()
    # sqliteConnection.close()
    # print("The SQLite connection is closed")
    # return records
    plist = []
    for i in id_list:
        product = Product.query.filter_by(id=i).all()
        plist.append(product)
    return plist


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
    print("ran runcmd")

def add_rose_pine_styles(overwrite: bool=False):
    # create style folder if not exists
    stylelib_path = f"{mpl.get_configdir()}/stylelib"
    Path(stylelib_path).mkdir(exist_ok=True)
    
    # download the styles from the github-repo if they don't exist
    for style in ["rose-pine-dawn.mplstyle", "rose-pine-moon.mplstyle", "rose-pine.mplstyle"]:
        filename = f"{stylelib_path}/{style}"
        if not overwrite and os.path.isfile(filename):
            continue
        # fetch and add to folder
        content = requests.get(f"https://raw.githubusercontent.com/h4pZ/rose-pine-matplotlib/main/themes/{style}").text
        with open(filename, "w+") as f:
            f.write(content)

def create_subplots(elem_dict):
    # product name: product emission, manufacturing emission

    X = list(elem_dict.keys())

    values = list(elem_dict.values())
    #emission per product
    products_emission = [i[0] for i in values]
    
    # 1
    Y1 = sum(products_emission)
    # 2
    Y2 = products_emission
    # 3
    Y3 = [i/(365*24) for i in products_emission]
    # 4
    Y4 = [i[0] for i in values]
    Y5 = [i[1] for i in values]
    
    figure, axis = plt.subplots(2, 2)
    
    # 1. Your total emission
    axis[0, 0].bar(['total emission'], Y1)
    axis[0, 0].set_title("Total Emission(kg/annum)")
    
    # 2. Emission per product
    axis[0, 1].bar(X, Y2)
    axis[0, 1].set_title("CO2 Emission per Product(kg/annum)")
    
    # 3. Hourly emission per device
    axis[1, 0].bar(X, Y3)
    axis[1, 0].set_title("Hourly Emission(kg) per Device")
    
    # 4. broken down emission - manufacturing+usage emission
    axis[1, 1].bar(X, Y5)
    axis[1, 1].bar(X, Y4,bottom=Y5)
    axis[1, 1].set_title("Usage(y) v Manufacturing Emission(r)")

    plt.subplots_adjust(hspace=0.5,wspace=0.5)

    # path exists
    if os.path.exists("api/static/chart.png"):
        os.remove("api/static/chart.png")
        plt.savefig("api/static/chart.png")
    else:
        plt.savefig("api/static/chart.png")

def api_func(country_id,yearly_pow):
    data = {
    "emission_factor": {
        "id": "electricity-energy_source_grid_mix",
        "region": f"{country_id}"
    },
    "parameters": {
        "energy": yearly_pow,
        "energy_unit": "kWh"
    }
    }

    url = "https://beta3.api.climatiq.io/estimate"
    api_key = os.environ.get('CLIMATIO_API_KEY')
    post_request = requests.post(url, json = data, headers = {"Authorization":f"Bearer {api_key}"})

    return post_request.json()

def calc_emission(duration,country_id,production_emission,power_duration,rating,quantiy):
    # returns emissions per device
    print(duration, country_id, production_emission, power_duration, rating, quantiy)
    daily_pow = (duration/power_duration)*rating*quantiy
    yearly_pow = daily_pow*365/1000
    yearly_pow = round(yearly_pow)
    post_response = api_func(country_id,yearly_pow)
    print(post_response)
    total_emissions = production_emission*quantiy + post_response['constituent_gases']['co2e_total']
    return total_emissions

@bp.route('/', methods=['GET'])
def result():
    cookie = request.cookies.get('uid')
    if cookie is not None:
        id_list = []
        with open(f'{cookie}.csv', 'r') as f:
            rl = f.readlines()
            # csv: country(country id), name(product id), quantity, time_used
            for i in rl:
                i = i.split(',')
                i = [*i[:-1], i[-1][:-1]]
                print(i)
                id_list.append(i[1])
            # expected average emission per entered product
            db_records = dbsearch(id_list)
        emission_dict = {}
        for elem in rl:
            elem = elem.split(',')
            elem = [*elem[:-1], elem[-1][:-1]]
            print(elem)
            for i in db_records:
                print('i:', i, "elem:", elem)
                if int(i[0].id) == int(elem[1]):
                    name,power_duration,production_emission,prod_rating = i[0].name,int(i[0].power_duration),int(i[0].production_emmission),float(i[0].power_rating)
                    break
            print(name, production_emission)
            prod_emission = calc_emission(int(elem[3]),elem[0],production_emission,power_duration,prod_rating,int(elem[2]))
            
            emission_dict[name] = prod_emission,production_emission
            products_emission = [i[0] for i in emission_dict.values()]
            total_emission = sum(products_emission)
            day_emmission = total_emission/(365)

            # 1
            Y1 = sum(products_emission)

            print(emission_dict)

        # runcmd("wget -P /tmp https://raw.githubusercontent.com/h4pZ/rose-pine-matplotlib/main/themes/rose-pine.mplstyle")
        add_rose_pine_styles(overwrite=False)

        print(plt.style.available)

        with plt.style.context("rose-pine"):
            create_subplots(emission_dict)

        resp = make_response(render_template('result.html', total_emission=total_emission, day_emmission=day_emmission))
        resp.set_cookie('uid', '', expires=0)
        os.remove(f'{cookie}.csv')
        return resp
    else:
        return redirect(url_for('index.index'))
