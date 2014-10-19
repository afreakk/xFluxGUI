from xceptions import Rxpt
import requests

class LongLatGetter(object):
    def __init__(self):
        pass

    def get_json_from_adress(self, place):
        try:
            data = requests.get('http://maps.google.com/maps/api/geocode/json?address=%s' % place ).json()
        except requests.exceptions.ConnectionError as l:
            raise Rxpt("Could not connect.\n"+l.__str__())
        if data['status'] != "OK":
            raise Rxpt("Not ok.")
        if len(data['results']) < 1:
            raise Rxpt("No results.")
        if len(data['results']) > 1:
            alternatives = "Too many results, be more specific.\nListing results:\n"
            i=0
            for x in data['results']:
                alternatives += ("[%i]"%i)+x['formatted_address']+"\n"
                i+=1
            raise Rxpt(alternatives)
        return data

    def get_lng_lat(self, place):
        data = self.get_json_from_adress(place)
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        locstr = data['results'][0]['formatted_address']
        return lat, lng, locstr
