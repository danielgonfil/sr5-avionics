import json
import requests

quickchart_url = 'https://quickchart.io/chart/create'

with open("adc_data.json","r") as data_file:
    post_data = json.load(data_file)

response = requests.post(url=quickchart_url,json=post_data)
response.raise_for_status()
print(response.json())