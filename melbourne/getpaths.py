import os
import csv
import pprint
import codecs
import melbourneroutedata

path = os.getcwd() + '2/shapes.txt'



RoutePathData = {} #data store
for route in melbourneroutedata.allRoutes: # loop through all the routes (only one exists in this scenario)
    RoutePathData[route] = [] # this will be a list of lists of {'lon':XXX, 'lat':XXX} dictionaries
    with codecs.open(path, 'rU', encoding='utf-8-sig') as rows:
        csvReader = csv.reader(rows)
        header = next(csvReader)
        route_id = header.index('shape_id')
        latIndex = header.index("shape_pt_lat")
        lonIndex = header.index("shape_pt_lon")
        for row in csvReader:
            if "2-FKN-A-mjp-1.5.H" == row[route_id]:
                lat = row[latIndex]
                lon = row[lonIndex]
                RoutePathData[route].append({'lat': lat, 'lon': lon}) # append this point to the path


# output all the data to a file named below:
fo = open('frankstonlinepath.py', 'w')
fo.write('frankstonlinepath = ' + pprint.pformat(RoutePathData))
fo.close()

print("Done")
