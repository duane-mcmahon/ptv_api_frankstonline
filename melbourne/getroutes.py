import os
import csv
import zipfile
import sys
import urllib
import codecs

# use the requests module to download the webpage
# (you can copy and paste this page into your browser to see it for yourself)
routes = {}  # this dictionary will store all the routes names and their titles

def dlProgress(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    sys.stdout.write("\r" + "...%d%%" % percent)
    sys.stdout.flush()


if not os.path.isfile('gtfs.zip'):
    req = urllib.urlretrieve('http://data.ptv.vic.gov.au/downloads/gtfs.zip', 'gtfs.zip', reporthook=dlProgress)
    # unzip from folder number 2 (which contains the relevant material)
    fh = open('gtfs.zip', 'rb')
    z = zipfile.ZipFile(fh)
    for name in z.namelist():  # To read the names of the files in an existing archive, use namelist()
        if name.startswith('2'):
            os.chdir(os.path.dirname(__file__))
            outpath = os.path.curdir
            z.extract(name, outpath)
    fh.close()
    #unzip subdir google_transit.zip


next_fh = open('2/google_transit.zip', 'rb')
z = zipfile.ZipFile(next_fh)
for name in z.namelist():
    outpath = os.path.curdir
    z.extract(name, outpath)

if not os.path.isfile('2/routes.txt'):
    #unzip subdir google_transit.zip
    path = os.getcwd() + '/2/google_transit.zip'
    next_fh = open(path, 'rb')
    z = zipfile.ZipFile(next_fh)
    for name in z.namelist():
        outpath = os.path.join(os.path.curdir, '2')
        z.extract(name, outpath)
    next_fh.close()

path = os.getcwd() + '/2/routes.txt'

with codecs.open(path, 'rU', encoding='utf-8-sig') as rows:
    csvReader = csv.reader(rows)
    header = next(csvReader)
    route_id = header.index('route_id')
    route_name = header.index('route_long_name')



# get frankston line for this example

    for row in csvReader:
        if "FKN" in row[route_id]:
            routes[row[route_id]] = row[route_name]



# save the routes dictionary to a text file (melbourneroutedata.py) to use later
import pprint

fo = open('melbourneroutedata.py', 'w')
fo.write('allRoutes = ' + pprint.pformat(routes))
fo.close()

sys.stdout.write("\r Done.")