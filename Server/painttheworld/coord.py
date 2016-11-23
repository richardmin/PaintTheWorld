from painttheworld.const import m1, m2, m3, m4, p1, p2, p3
import math

def conversion_rates(coord):
    """Calculates the conversion rate for 1 degree of longitude to a variety
    of measurements, returned in a dict. 
        
    Args: 
        coord: a tuple (longitude, latitude) 
    Returns:
        Conversion rate for 1 degree of longitude to miles
    """
    latitude = math.radians(coord[1])
    dict = {}

    latlen = m1 + ( m2 * math.cos(2 * latitude) + \
                    m3 * math.cos(4 * latitude) + \
                    m4 * math.cos(6 * latitude)   \
                  )

    longlen = (p1 * math.cos(1 * latitude)) + \
              (p2 * math.cos(3 * latitude)) + \
              (p3 * math.cos(5 * latitude))

    dict['lat_meters'] = latlen
    dict['lat_feet'] = latlen * 3.28083333
    dict['lat_miles'] = dict['lat_feet'] / 5280
    
    dict['long_meters'] = longlen
    dict['long_feet'] = longlen * 3.28083333
    dict['long_miles'] = dict['long_feet'] / 5280

    return dict

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Source code from: http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km
