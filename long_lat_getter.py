import requests
class Rxpt(Exception):
    pass

class LongLatGetter(object):
    def __init__(self):
        pass
    def get_lng_lat(self, place):
        print "searching for %s"%place
        data = requests.get('http://maps.google.com/maps/api/geocode/json?address=%s' % place ).json()
        if data['status'] != "OK":
            raise Rxpt("Not ok.")
        if len(data['results']) < 1:
            raise Rxpt("No results.")
        if len(data['results']) > 1:
            alternatives = "Too many results, specify better.\nResults:\n"
            for x in data['results']:
                alternatives += x['formatted_address']+"\n"
            raise Rxpt(alternatives)
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng

