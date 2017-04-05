# a module that will calculate sun & moon rise & set times to help define the start time of a timelapse
# uses the ephem module for celestial calcs and geopy for location to lat/long conversion
import ephem
from datetime import datetime
import time

def event(event_type, lat, lon):

    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)

    local_now = time.time()
    utc_offset = datetime.fromtimestamp(local_now) - datetime.utcfromtimestamp(local_now)

    event_dict = { 'sunset': [ephem.Sun, observer.next_setting],
                  'sunrise': [ephem.Sun, observer.next_rising],
                  'moonset': [ephem.Moon, observer.next_setting],
                  'moonrise': [ephem.Moon, observer.next_rising] }

    body = event_dict[event_type][0]()
    utc_sunset_time = ephem.Date(event_dict[event_type][1](body))

    event_time = utc_sunset_time.datetime() + utc_offset
    # print "Today the sun will set @ {}".format(datetime.strftime(now, "%Y/%m/%d %H:%M:%S"))
    return event_time
