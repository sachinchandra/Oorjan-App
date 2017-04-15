import numpy as np
import json
import glob
import os
import sys
from datetime import datetime, timedelta
import requests
from conf import api_host, api_port

folder = sys.argv[-2]
is_reference_data = sys.argv[-1].lower() in ('yes', 'true', 't', 'y')

path = os.path.join(folder, "*.json")
for i, fname in enumerate(glob.glob(path)): 
    data = json.load(open(fname))
    dc_data = data['outputs']['dc']

    dc_data = np.array(dc_data).reshape((365, 24))

    dc_mean = np.mean(dc_data, axis=0)
    dc_std = np.std(dc_data, axis=0)

    sample = np.random.normal(dc_mean, dc_std, size=(365, 24))
    sample[sample<0] = 0

    dc_sample = list(sample.flatten())

    location = data['station_info']['location']
    city = data['station_info']['city']
    timeStamp = 'Jan 1 2017 12:00AM'
    datetime_object = datetime.strptime(timeStamp, '%b %d %Y %I:%M%p')

    for d in dc_sample:
        r = requests.post("http://{host}:{port}/adddata".format(host=api_host, port=api_port),
                              data={'location': location, 'city': city,
                                    'solarid': i+ 1, 'dc': d,
                                    'timestamp': datetime_object,
                                    'isreferencedata' : is_reference_data})
        datetime_object = datetime_object + timedelta(hours = 1)
