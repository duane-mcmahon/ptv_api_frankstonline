import os
import csv
import codecs



def getArrivals(stopID):
    returnValue = []
    path = os.getcwd() + '/melbourne/2/stop_times.txt'

    with codecs.open(path, 'rU', encoding='utf-8-sig') as rows:
        csvReader = csv.reader(rows)
        csvReader = csv.reader(rows)
        header = next(csvReader)
        arrival = header.index('arrival_time')
        departure = header.index('departure_time')
        stop_id = header.index('stop_id')
        for row in csvReader:
            if row[3] == stopID:
                returnValue.append(row[1])

        return returnValue


