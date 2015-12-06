import pprint
import os
import csv
import codecs
import melbourneroutedata
import json

infile = open("stations.txt").readlines()
path = os.getcwd() + '/2/stops.txt'
allRoutesStopData = {} #dictionary

with codecs.open(path, 'rU', encoding='utf-8-sig') as rows:
    csvReader = csv.reader(rows)
    csvReader = csv.reader(rows)
    header = next(csvReader)
    stop_id = header.index('stop_id')
    stop_name = header.index('stop_name')
    stop_lat = header.index('stop_lat')
    stop_lon = header.index('stop_lon')

    for route in melbourneroutedata.allRoutes:
        allRoutesStopData[route] = []
        for row in csvReader:
            for line in infile:
                station = row[stop_name].rsplit('Railway', 1)[0]
                line_st = line.rsplit('Station', 1)[0]
                if line_st == station:
                    #print('{:s} is in {:s}'.format(line_st, station))
                    allRoutesStopData[route].append({"lat": row[stop_lat], "lon": row[stop_lon], "stopId": row[stop_id], "title": row[stop_name]})
        unique = set()
        for d in allRoutesStopData[route]:
            t = tuple(d.items())
            unique.add(t)
        allRoutesStopData[route] = [dict(x) for x in unique]

for key, value in allRoutesStopData.iteritems():
    if value:
        print json.dumps(value)
# output all the data to a file named:
fo = open('frankstonlinestops.py', 'w')
fo.write('frankstonlinestops = ' + pprint.pformat(allRoutesStopData))
fo.close()

