import json
import os
import sys
from pprint import pprint
import glob
import requests
from datetime import datetime, timedelta
from conf import api_host, api_port


folder = sys.argv[-2]
is_reference_data = sys.argv[-1].lower() in ('yes', 'true', 't', 'y')

# read json file and populate database
path = os.path.join(folder, "*.json")

for fname in glob.glob(path):
    with open(fname) as data_file:
        data = json.load(data_file)

        location = data['station_info']['location']
        city = data['station_info']['city']
        timeStamp = 'Jan 1 2017 12:00AM'
        datetime_object = datetime.strptime(timeStamp, '%b %d %Y %I:%M%p')

        for d in data['outputs']['dc']:
            r = requests.post("http://{host}:{port}/adddata".format(host=api_host, port=api_port),
                              data={'location': location, 'city': city,
                                    'solarid': "", 'dc': d,
                                    'timestamp': datetime_object,
                                    'isreferencedata': is_reference_data})
            datetime_object = datetime_object + timedelta(hours=1)
