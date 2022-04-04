import time
import pandas as pd

def get_lat_lng(apiKey, address):
    import requests
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'
           .format(address.replace(' ','+'), apiKey))
    try:
        response = requests.get(url)
        resp_json_payload = response.json()
        lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        lng = resp_json_payload['results'][0]['geometry']['location']['lng']
        adds = resp_json_payload['results'][0]['formatted_address']

    except:
        print('ERROR: {}'.format(address))
        lat = 0
        lng = 0
        adds = 'error'

    return lat, lng, adds

if __name__ == '__main__':
    # get key
    fname = 'GoogleMapsAPIKey.txt'
    file  = open(fname, 'r')
    apiKey = file.read()

lat_res = []
log_res = []
adds_res = []

# regex clear address_cn_clear removing duplicated and unusable address
filepath = 'address_cn_clear.txt'
with open(filepath, encoding="utf8") as fp:
    for line in fp:
        sing_add = line.strip()
        if sing_add == 'O':
            geo_info = ['nan','nan','nan']
        elif line == "\n":
            geo_info = ['nl','nl','nl']
        else:
            geo_info = get_lat_lng(apiKey, address=sing_add)
        lat_res.append(geo_info[0])
        log_res.append(geo_info[1])
        adds_res.append(geo_info[2])
        time.sleep(0.1)

lat_log_adds = pd.DataFrame(
    {'LAT': lat_res,
     'LOG': log_res,
     'ADDRESS': adds_res
    })

lat_log_adds.to_csv("lla_all_cn.csv", encoding='utf-8', index=False)
