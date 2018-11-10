import urllib.request
import json
import math
import pandas as pd

#start of URL
DESTINATION_URL_BASE = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
GEO_URL_BASE = 'https://maps.googleapis.com/maps/api/geocode/json?'

#key
api_key = 'AIzaSyCz_fTLy-L-adRcPTOqqXfOFyBBMex6UkM'
DONE_api_key = '&key=' + api_key

#Destination dataframe
destinationsDF = pd.DataFrame(columns=['name', 'geolocation'])


class RadiusMap:

                                   #Address            #Meters
    def __init__(self, start_address: str, search_radius: int, destination_types: list):
        self.start_address = start_address
        self.search_radius = search_radius
        self.destination_types = destination_types

        self.DONE_start_address = 'address=' + start_address.replace(' ', '+')
        self.DONE_search_radius = '&radius=' + str(search_radius)

        #initialize map with no start_geo and no DONE_start_geo
        self.start_geo = None
        self.DONE_start_geo = None

        #initialize destinations as None
        self.destinations = None

        #initialzie destinations_dataframe as None
        self.destinations_dataframe = None


    def get_start_address(self):
        return self.start_address

    def get_search_radius(self):
        return self.search_radius

    def get_destination_types(self):
        return self.destination_types

    '''
    def get_distance(self, lat: (float, float), lng: (float, float)):
        R = 6378.137

        dLat = lat2 * math.pi / 180 - lon1 * math.pi / 180
        dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
        a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(Lat1 * math.pi / 100) * math.cos(
            Lat2 * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return (d * 1000)
    '''

    def set_start_geo(self, start_coord: (float, float), search_radius: float):
        return self.start_geo

    def generate_destinations_dataframe(self):
        """ ONLY CALL THIS FUNCTION AFTER GENERATING STARTING GEOLOCATION
            IT WILL NOT WORK OTHERWISE. YOU HAVE BEEN WARNED!!"""
        self.destinations_dataframe = pd.DataFrame(columns=['name', 'geolocation'])

        for i in self.get_destination_types():

            '''For each type of destination, request name and geolocation'''
            destination_type = i
            DONE_destination_type = '&type=' + destination_type

            destinations_request = DESTINATION_URL_BASE + self.DONE_start_geo + DONE_destination_type + self.DONE_search_radius + DONE_api_key
            destinations_response = urllib.request.urlopen(destinations_request).read()
            destinations_json = json.loads(destinations_response)

            for j in range(0, len(destinations_json['results'])):
                lat = str(destinations_json['results'][j]['geometry']['location']['lat'])
                lng = str(destinations_json['results'][j]['geometry']['location']['lng'])

                geo_location = lat + ',' + lng

                name = str(destinations_json['results'][j]['name'])

                tempDF = pd.DataFrame({'name':[name], 'geolocation': [geo_location]})

                self.destinations_dataframe = self.destinations_dataframe.append(tempDF)

        self.destinations_dataframe = self.destinations_dataframe.reset_index(drop=True)
        print(self.destinations_dataframe, "\n")



    def generate_start_geo(self):
        '''Convert address into latitude and longitude
                            Create geo request url'''
        start_geo_request = GEO_URL_BASE + self.DONE_start_address + DONE_api_key

        # Get Response from geo request
        start_geo_response = urllib.request.urlopen(start_geo_request).read()

        # Load response into JSON
        start_geo_json = json.loads(start_geo_response)

        # Finally, Get start_geo lattitude and longitude
        lat = str(start_geo_json['results'][0]['geometry']['location']['lat'])
        lng = str(start_geo_json['results'][0]['geometry']['location']['lng'])

        self.start_geo = lat + ',' + lng
        self.DONE_start_geo = 'location=' + self.start_geo

if __name__ == "__main__":
    Map = RadiusMap("952 Olive Street Eugene, OR 97401", 800, ["library"])
    Map.generate_start_geo()
    Map.generate_destinations_dataframe()




