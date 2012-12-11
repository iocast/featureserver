import sys
import operator
import os
import urllib
import simplejson
import random
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    import cStringIO as StringIO
except:
    import StringIO

from FeatureServer.Server import Server
from FeatureServer.DataSource.SQLite import SQLite


url = len(sys.argv) > 1 and sys.argv[1] or "http://localhost:8080/scribble"




def test_POST():

    data = simplejson.loads('{"crs": {"type": "none", "properties": {"info": "No CRS information has been provided with this data."}}, "type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [-121.232, 42.122999999999998]}, "type": "Feature", "id": 1, "properties": {"strokeColor": "red", "title": "Feature 3", "author": "Your Name Here"}}]}')

    random_x = random.random() * 100
    random_y = random.random() * 10
    data['features'][0]['geometry']['coordinates'] = [random_x, random_x]

    urllib.urlopen(url, simplejson.dumps(data)).read()
    all_data = urllib.urlopen(url).read()
    all_features = simplejson.loads(all_data)
    f = sorted(all_features['features'], key=operator.itemgetter('id'))[-1]
    assert f['geometry']['coordinates'][0] == random_x


def setup():
    pass

def teardown():
    pass



if __name__ == "__main__":
    setup()

    test_POST() 


    teardown()
