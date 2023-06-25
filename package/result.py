import os
import matplotlib.pyplot as plt
import subprocess
from flask import Blueprint, make_response, redirect, render_template, request, url_for
import sqlite3
import requests
from dotenv import load_dotenv

from package.models.product import Product

bp = Blueprint('result', __name__)
load_dotenv()

def dbsearch(id_list:list):
    try:
        sqliteConnection = sqlite3.connect('../instance/database.db')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select * from devices where dev_id in {}".format(id_list)
        cursor.execute(sqlite_select_Query)
        # dev_id, deviceName, productEmission, powerRating, powerDuration
        records = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
            return records


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

def create_subplots(names,data_user,data_man):
    # create data
    x = [i[1] for i in names]
    y1 = [10, 20, 10, 30]
    y2 = [20, 25, 15, 25]
    
    # plot bars in stack manner
    plt.bar(x, y1)
    plt.bar(x, y2, bottom=y1)
    plt.xlabel("Product")
    plt.ylabel("CO2 Emission(kg/annum)")
    plt.legend(["Your yearly emission", "Product Manufacturing emission"])
    plt.title("CO2 Emissions")

    # path exists
    if os.path.exists("package/static/chart.png"):
        os.remove("package/static/chart.png")
        plt.savefig("package/static/chart.png")
    else:
        plt.savefig("package/static/chart.png")

def api_func():
    data = {
    "emission_factor": {
        "id": "electricity-energy_source_grid_mix",
        "region": "$regionCode" #$regionCode is a string value based on the location provided by the user
    },
    "parameters": {
        "energy": "$energyconsumption", #$energyconsumption - yearly usage is an int value (so remove the quotes here) based on calculations mentioned in the whataspp message, do note reals have to be rounded off
        "energy_unit": "kWh"
    }
    }

    url = "https://beta3.api.climatiq.io/estimate"
    api_key = os.environ.get('CLIMATIO_API_KEY')
    post_request = requests.post(url, json = data, headers = {f"Authorization":"Bearer {api_key}"}) #$API_KEY is the api key

    post_response = post_request.json()
    print(post_response)

    """
    in the post_response there is a dictionary like this -
    "constituent_gases": {
    "co2e_total": 2496.2,
    "co2e_other": null,
    "co2": 2496.2,
    "ch4": null,
    "n2o": null
    }

    from this we can pick up the co2e_total value which gives the carbon emissions (CO2 and equivalents) in the kg CO2e unit.
    """

def calc_emission(duration,country_id,power_duration,rating,quantiy):

    daily_pow = (duration/power_duration)*rating*quantiy
    yearly_pow = daily_pow*365/1000
    yearly_pow = round(yearly_pow)

    # api_func() call -> return



@bp.route('/', methods=['GET'])
def result():
    cookie = request.cookies.get('uid')
    if cookie is not None:
        id_list = []
        with open(f'{cookie}.csv', 'r') as f:
            rl = f.readlines()
            # csv: country(country id), name(product id), quantity, time_used
            for i in rl:
                i = i.split()
                i = [*i[:-1], i[-1][:-1]]
            for i in rl:
                id_list.append(i[1])
            # expected average emission per entered product
            db_records = dbsearch(id_list)
            # TODO: get list of emissions for user from api

        with plt.style.context("/tmp/rose-pine.mplstyle"):
            create_subplots(id_list,user_records,db_records)

        resp = make_response(render_template('result.html'))
        resp.set_cookie('uid', '', expires=0)
        os.remove(f'{cookie}.csv')
        return resp
    else:
        return redirect(url_for('index.index'))
