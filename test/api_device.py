#note install requests lib from pip if not done already
import requests

data = {
  "emission_factor": {
    "id": "electricity-energy_source_grid_mix",
    "region": "IN" #$regionCode is a string value based on the location provided by the user
  },
  "parameters": {
    "energy": 1000, #$energyconsumption - yearly power usage is an int value (so remove the quotes here) based on calculations mentioned in the whataspp message, do note reals have to be rounded off
    "energy_unit": "kWh"
  }
}

url = "https://beta3.api.climatiq.io/estimate"

post_request = requests.post(url, json = data, headers = {"Authorization":"Bearer 4YSKREM0F84Z8VPRVD1TV062Q9ZR"}) #$API_KEY is the api key

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
