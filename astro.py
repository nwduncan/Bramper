# a module that will calculate sun & moon rise & set times to help define the start time of a timelapse
# uses the ephem module for celestial calcs and geopy for location to lat/long conversion
import ephem
from geopy import geocoders
from datetime import datetime
import time

class Event(object):
    def __init__(self):
        pass

def spacetime(address):
    geoloc = geocoders.Nominatim()
    loc = geoloc.geocode(address)
    lat, lon = loc.latitude, loc.longitude

    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)

    local_now = time.time()
    utc_offset = datetime.fromtimestamp(ts_now) - datetime.utcfromtimestamp(ts_now)

    return observer, utc_offset


def sunset():

    observer, utc_offset =

    sun = ephem.Sun()
    utc_sunset_time = ephem.Date(observer.next_setting(sun))

    now = utc_sunset_time.datetime() + diff
    # print "Today the sun will set @ {}".format(datetime.strftime(now, "%Y/%m/%d %H:%M:%S"))
    return now
