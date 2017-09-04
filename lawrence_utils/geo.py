## get key from here 
## https://developers.google.com/maps/documentation/javascript/get-api-key?hl=zh-tw
import requests	

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