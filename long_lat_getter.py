import requests
import exceptions
class Rxpt(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class LongLatGetter(object):
    def __init__(self):
        pass
    def get_lng_lat(self, place):
        print "searching for %s"%place
        try:
            data = requests.get('http://maps.google.com/maps/api/geocode/json?address=%s' % place ).json()
        except requests.exceptions.ConnectionError as l:
            raise Rxpt(l.__str__())
        if data['status'] != "OK":
            raise Rxpt("Not ok.")
        if len(data['results']) < 1:
            raise Rxpt("No results.")
        if len(data['results']) > 1:
            alternatives = "Too many results, be more specific.\nResults:\n"
            for x in data['results']:
                alternatives += x['formatted_address']+"\n"
            raise Rxpt(alternatives)
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng

