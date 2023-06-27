import os
import os.path
import requests
from pathlib import Path
import matplotlib as mpl
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from flask import Blueprint, make_response, redirect, render_template, request, url_for

from api.models.product import Product

bp = Blueprint('result', __name__)
load_dotenv()

def add_rose_pine_styles(overwrite: bool=False):
    stylelib_path = f"{mpl.get_configdir()}/stylelib"
    Path(stylelib_path).mkdir(exist_ok=True)
    
    for style in ["rose-pine-dawn.mplstyle", "rose-pine-moon.mplstyle", "rose-pine.mplstyle"]:
        filename = f"{stylelib_path}/{style}"
        if not overwrite and os.path.isfile(filename):
            continue
        content = requests.get(f"https://raw.githubusercontent.com/h4pZ/rose-pine-matplotlib/main/themes/{style}").text
        with open(filename, "w+") as f:
            f.write(content)

def create_subplots(elem_dict):
    X = list(elem_dict.keys())
    values = list(elem_dict.values())
    products_emission = [i[0] for i in values]
    
    Y1 = sum(products_emission)
    Y2 = products_emission
    Y3 = [i/(365*24) for i in products_emission]
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
    API_KEY = os.environ.get('CLIMATIO_API_KEY')
    post_request = requests.post(url, json = data, headers = {"Authorization":f"Bearer {API_KEY}"})

    return post_request.json()

# returns emissions per device
def calc_emission(duration,country_id,production_emission,power_duration,rating,quantity):
    daily_pow = (duration/power_duration)*rating*quantity
    yearly_pow = round(daily_pow*365/1000)
    post_response = api_func(country_id,yearly_pow)
    print(post_response)
    total_emissions = production_emission*quantity + post_response['constituent_gases']['co2e_total']
    return total_emissions

@bp.route('/', methods=['GET'])
def result():
    cookie = request.cookies.get('uid')
    if cookie is not None:
        emission_dict = {}
        with open(f'{cookie}.csv', 'r') as f:
            rl = f.readlines()
            for i in rl:
                i = i.split(',')
                i = [*i[:-1], i[-1][:-1]]
                product = Product.query.filter_by(id=i[1]).all()
                name,power_duration,production_emission,prod_rating = product[0].name,int(product[0].power_duration),int(product[0].production_emmission),float(product[0].power_rating)
                prod_emission = calc_emission(int(i[3]),i[0],production_emission,power_duration,prod_rating,int(i[2]))
                emission_dict[name] = prod_emission,production_emission
                
            products_emission = [i[0] for i in emission_dict.values()]
            total_emission = sum(products_emission)
            day_emmission = total_emission/365

        add_rose_pine_styles(overwrite=False)
        with plt.style.context("rose-pine"):
            create_subplots(emission_dict)

        resp = make_response(render_template('result.html', total_emission=total_emission, day_emmission=day_emmission))
        resp.set_cookie('uid', '', expires=0)
        os.remove(f'{cookie}.csv')
        os.remove(f'{cookie}-flight.csv')
        return resp
    else:
        return redirect(url_for('index.index'))
