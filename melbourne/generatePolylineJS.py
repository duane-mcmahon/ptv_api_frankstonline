import frankstonlinepath
import random

COLORS = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF', '#800000', '#008000', '#000080', '#808000', '#008080', '#800080']

fo = open('../static_assets/polylineJS.js', 'w')

routeColor = random.choice(COLORS) # choose a random color for this route's paths
latlngJavaScript = []
for key, value in frankstonlinepath.frankstonlinepath.items():
    for pair in value:
        place = 'new google.maps.LatLng({:s}, {:s})'.format(pair['lat'], pair['lon'])
        print(place)
        latlngJavaScript.append(place)
    latlngJavaScript = ', '.join(latlngJavaScript)

    polylineJavaScript = """var routePath = new google.maps.Polyline({
    path: [%s],
    strokeColor: '%s',
    strokeOpacity: 1.0,
    strokeWeight: 2
  });""" % (latlngJavaScript, routeColor)

    fo.write(polylineJavaScript)
fo.close()
