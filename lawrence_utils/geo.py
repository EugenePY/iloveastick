## get key from here 
## https://developers.google.com/maps/documentation/javascript/get-api-key?hl=zh-tw
import requests	
from utils import *

def geocoding(address):

    key = '<>'
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(address,key)
    res = requests.post(url).json()
    return res['results'][0]['geometry']['location']['lat'], res['results'][0]['geometry']['location']['lng']


## to cal. distance
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km


## get key here :
## https://developers.google.com/places/web-service/get-api-key?hl=zh-tw

def get_restaurant_nearby(lat='25.035135',lon='121.54388',keywords):
    lat = '25.035135'
    lon = '121.54388'
    radius = 499
    key = "AIzaSyB3VPhVziriK6K8ObknA9RzP0wGz46-ocs"
    keywords = "牛排"
    keywords = urllib.parse.quote(keywords, safe='')
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type=restaurant&keyword={}&key={}".format(lat,lon,radius,keywords,key)
    res = requests.get(url).json()
    results = res['results']

    next_page_token = value_for_keypath(res,'next_page_token',default=None)

    i =1 
    while True:
        i+=1
        print(i)
        print(next_page_token)
        if next_page_token:
            url_tmp = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}".format(next_page_token,key)
            res_tmp = requests.get(url).json()
            results_tmp = res_tmp['results']        
            results.extend(results_tmp)
            next_page_token = value_for_keypath(res_tmp,'next_page_token',default=None)
        else:
            break
    return results
