import googlemaps
import json
from pprint import pprint
import os

key = os.environ.get('GOOGLEMAPS_API_KEY')
gmaps = googlemaps.Client(key = key)

############ Reference point
def get_geocode(reference_place):
    geocode = gmaps.geocode(address=reference_place)
    # pprint(geocode)
    return geocode

############ extract coordinates
def get_coord(geocode):
    # print(coord)
    return geocode[0]['geometry']['location']

########### extract places
def get_places(query_place, coord, radius: int = 25, language: str="spanish"):
    # with places
    places = gmaps.places(query=query_place, location=coord, radius=radius, open_now=True, language=language)

    # with places nearby
    places2 = gmaps.places_nearby(keyword=query_place, location=coord, radius=radius, open_now=True, language=language)

    nearby_places = []
    place_names = []
    place_ids = []
    for place in places['results']:
        nearby_places.append({place['place_id']: place['name']})
        place_names.append(place['name'])
        place_ids.append(place['place_id'])

    # print(nearby_places)
    # print(place_names)
    return nearby_places, place_names, place_ids

########### getting directions 
def get_directions(origin, place_id, mode: str = "walking"):
    direction = gmaps.directions(origin=origin, destination=f"place_id:{place_id}", mode=mode)
    # pprint(direction)

    distance = direction[0]['legs'][0]['distance']['text']
    duration = direction[0]['legs'][0]['duration']['text']
        
    return distance, duration

########### extract place info
def get_place_info(origin, place_names, place_ids, mode: str = "walking"):
    # print(place_id)
    places_info = []
    places_reviews = []

    for i in range(len(place_names)):
        place_info = {}
        distance, duration = get_directions(origin, place_ids[i], mode=mode)
        place = gmaps.place(place_id=place_ids[i])
        try:
            rating = place['result']['rating']
        except KeyError:
            rating = None
        try:
            reviews = place['result']['reviews']
            text_reviews = []
            for review in reviews:
                text_reviews.append(review["text"])
        except KeyError:
            text_reviews = None
        place_info["distance"] = distance
        place_info["duration"] = duration
        place_info["rating"] = rating
        # place_info["reviews"] = text_reviews
        places_info.append({place_names[i]: place_info})
        places_reviews.append({place_names[i]: text_reviews})
        # print(places_info)

    # json_object = json.dumps(places_info, indent=4)
    # with open("places-50-m.json", "w") as outfile:
    #     outfile.write(json_object)
    # json_object2 = json.dumps(places_reviews, indent=4)
    # with open("reviews-50-m.json", "w") as outfile:
    #     outfile.write(json_object2)

    return places_info, places_reviews