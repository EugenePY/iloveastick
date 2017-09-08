import requests 
from utils import *
from math import radians,  cos, sin, asin, sqrt

## get key from here 
## https://developers.google.com/maps/documentation/javascript/get-api-key?hl=zh-tw

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

def value_for_keypath(input_, keypath, value_type=None, *args, **kwargs):
    """
    Args:
        keypath: keypath for value
        value_type: convert value to type, use `None` for not convert
        default: default value if value not available, including keypath is
            invalid and/or value is `None`

    Returns:
        returned value

    Raises:
        ValueNotAvailableError: raised if "default" not in kwargs
    """
    paths = keypath.split(".")
    ret = input_
    try:
        for p in paths:
            try:
                ret = ret[p]
            except (KeyError, TypeError):
                raise ValueNotAvailableError("{}: {}".format(paths, p))
            if ret is None:
                raise ValueNotAvailableError("{}: {}".format(paths, p))
    except:
        if "default" in kwargs:
            ret = kwargs["default"]
        else:
            raise

    if value_type and ret is not None:
        try:
            ret = value_type(ret)
        except ValueError:
            return None

    return ret 

def find_resturant_nearby(keywords,lon=121.5290,lat=25.0436,per_page=50,dis_range=5,order_by='hits'):
    keywords = '&'.join(keywords.split(" "))

    url = "https://emma.pixnet.cc/blog/articles/search?key={}&per_page={}&type=tag".format(keywords,per_page)
    response = requests.get(url).json()

    items=[]
    for article in response['articles']:
        item = OrderedDict()
        item['address'] = value_for_keypath(article,'address',default=None)
        item['hits'] = value_for_keypath(article,'hits.total',default=None)

        item['title'] = value_for_keypath(article,'title',default=None)
        item['lon'] = value_for_keypath(article,'location.longitude',default=None)
        item['lat'] = value_for_keypath(article,'location.latitude',default=None)
        items.append(item)


    df = pd.DataFrame(items)
    df = df.dropna(subset=df.columns)

    df['distance'] = df.apply(lambda row: haversine(row['lon'], row['lat'], lon,lat), axis=1)
    df = df.query('distance<{}'.format(dis_range))
    df = df.query('distance<{}'.format(dis_range))
    df.sort([order_by],ascending=[False])

    return df


def add_google_info(df):
    _name=[]
    _type=[]
    _open_hour=[]
    _rating=[]

    for title in df['title']:
        url = 'https://www.google.com.tw/search?q={}'.format(title)
        response = requests.get(url)
        tree = html.fromstring(response.text)
        try:
            tmp = tree.xpath("//div[@class='_B5d']/text()")[0]
        except:
            tmp = ''
        _name.append(tmp)

        try:
            tmp = tree.xpath("//div[@class='_POh']/span/text()")[0]
        except:
            tmp = ''
        _type.append(tmp)

        try:
            tmp = tree.xpath("//span[@class='_bO']/following-sibling::span[@class='_tA']/text()")[1]
        except:
            tmp = ''
        _open_hour.append(tmp)

        try:
            tmp = tree.xpath("//span[@class='_kgd']/text()")[0]
        except:
            tmp = ''
        _rating.append(tmp)

    df['name'] = _name
    df['type'] = _type
    df['open_hour'] = _open_hour
    df['rating'] = _rating

    return df