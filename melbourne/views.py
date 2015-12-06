from django.http import HttpResponse
from django.shortcuts import render
import requests
import time
import datetime
from dateutil.parser import parse
from django.shortcuts import render_to_response
from django.template import RequestContext
import frankstonlinestops
import json
import logging
import logging.config
import getStationDepartures
import operator
from client import PTVClient
import apikey


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'NOTSET',
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'ERROR'
        }
    }
}

logging.config.dictConfig(LOGGING)


def index(request):
    jdata = []
    resultdata = []
    stations = []
    for key, value in frankstonlinestops.frankstonlinestops.iteritems():
        if value:
            jdata = json.dumps(value)
    if request.method == 'POST':
        client = PTVClient(developer_id=apikey.devid, api_key=apikey.devkey)

        logger = logging.getLogger(__name__)
        logger.debug('Here is the post data:\n %s', json.dumps(request.POST, indent=4, sort_keys=True))
        departureTime = request.POST.get('travelTime')
        hoursmins = time.strftime('%H:%M:%S', time.strptime(departureTime, '%I:%M:%S %p'))
        departureTime = str(request.POST.get('travelDate')) + " " + hoursmins
        client.set_time(departureTime)
        latitude = request.POST.get('departurePointLat', '')
        longitude = request.POST.get('departurePointLon', '')
        departurePoint = client.stops_nearby((latitude, longitude), mode='train')[0]
        latitude = request.POST.get('destinationPointLat', '')
        longitude = request.POST.get('destinationPointLon', '')
        destinationPoint = client.stops_nearby((latitude, longitude), mode='train')[0]
        departures = departurePoint.broad_next_departures(limit=12)
        deps_arrivals = {}
        stations.append(departurePoint.location_name)
        stations.append(destinationPoint.location_name)
        for departure in departures:
            obj = departure['run']
            results = client.stopping_pattern('train', obj.run_id, departurePoint.stop_id, for_utc=None)
            for destination_arrival in results:
                platform = destination_arrival['platform']
                # check that the time of departure is after required departure time (begin refining results)
                if platform.stop.stop_id == destinationPoint.stop_id:
                    time_obj = destination_arrival['time_timetable_utc']
                    tempstring = (str(time_obj)[:-6])
                    temp_date = departure['time_timetable_utc']
                    date1 = parse(str(temp_date)[:-6])  # available departure time
                    date2 = parse(departureTime)  # requested departure time
                    date3 = parse(str(time_obj)[:-6])  # destination time

                    if (date1.time() > date2.time()) and (date3.time() > date2.time()) and (date1.time() < date3.time()):
                        deps_arrivals[str(departure['time_timetable_utc'])[:-6]] = tempstring

        logger.debug(deps_arrivals)
        sorted_x = sorted(deps_arrivals.items(), key=operator.itemgetter(0))

        if sorted_x:
            resultdata = json.dumps(sorted_x[0])

        if stations:
            logger.debug(json.dumps(stations))
        return render_to_response("index.html",
                                  {"jdata": jdata, "resultdata": resultdata, "stations": json.dumps(stations)},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response("index.html", {"jdata": jdata}, context_instance=RequestContext(request))