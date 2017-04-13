import json
from pprint import pprint
import requests
from datetime import datetime, timedelta

#read json file and populate database
with open('data.json') as data_file:    
    data = json.load(data_file)

    location = data['station_info']['location']
    city = data['station_info']['city']
    timeStamp = 'Jan 1 2016 12:00AM'
    solarid = 1
    datetime_object = datetime.strptime(timeStamp, '%b %d %Y %I:%M%p')

    for d in data['outputs']['dc']:
    	datetime_object = datetime_object + timedelta(hours= 1)
    	r = requests.post("http://localhost/addData", data={'location': location, 'city': city, 'solarid': solarid, 'dc': d, 'timestamp': datetime_object})

  

    

