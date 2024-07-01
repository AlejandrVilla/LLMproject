import googlemaps
import json
from pprint import pprint
import os

key = os.environ.get('GOOGLEMAPS_API_KEY')
gmaps = googlemaps.Client(key = key)

############ Reference point
def get_geocode(reference_place):
    geocode = gmaps.geocode(address=reference_place)
    return geocode

############ extract coordinates
def get_coord(geocode):
    return geocode[0]['geometry']['location']

########### extract places for get-recomendation
def get_places(query_place, coord, radius: int = 25, language: str="spanish"):
    # with places
    # places = gmaps.places(query=query_place, location=coord, radius=radius, open_now=False, language=language)

    # with places nearby
    places = gmaps.places_nearby(keyword=query_place, location=coord, radius=radius, open_now=False, language=language)

    nearby_places = []
    place_names = []
    place_ids = []
    if places['status'] != "ZERO_RESULTS":
        for place in places['results']:
            nearby_places.append({place['place_id']: place['name']})
            place_names.append(place['name'])
            place_ids.append(place['place_id'])

    return nearby_places, place_names, place_ids

########### getting directions 
def get_directions(origin, place_id, mode: str = "walking"):
    direction = gmaps.directions(origin=origin, destination=f"place_id:{place_id}", mode=mode)

    distance = direction[0]['legs'][0]['distance']['text']
    duration = direction[0]['legs'][0]['duration']['text']
        
    return distance, duration

########### extract place info for get-recomendation
def get_place_summary(place_name, place_id):
    place_info = {}
    place = gmaps.place(place_id=place_id)
    try:
        rating = place['result']['rating']
    except KeyError:
        rating = None
    try:
        maps_url = place['result']['url']
    except KeyError:
        maps_url = None
    try:
        phone_number = place['result']['international_phone_number']
    except KeyError:
        phone_number = None
    try:
        opened = place['result']['current_opening_hours']['open_now']
    except KeyError:
        opened = None
    place_info = {
        "name": place_name,
        "place_id": place_id,
        "rating": rating,
        "maps_url": maps_url,
        "phone_number": phone_number,
        "opened": opened
    }

    # json_object = json.dumps(place_info, indent=4)
    # with open("places_info.json", "w") as outfile:
    #     outfile.write(json_object)

    return place_info

########### extract place info for get-plan
def get_place_info(origin, place_name, place_id, mode: str = "walking"):
    place_reviews = []
    place_info = {}

    distance, duration = get_directions(origin, place_id, mode=mode)
    place = gmaps.place(place_id=place_id)
    try:
        rating = place['result']['rating']
    except KeyError:
        rating = None
    try:
        location = place['result']['geometry']['location']
    except KeyError:
        location = None
    try:
        reviews = place['result']['reviews']
        text_reviews = []
        for review in reviews:
            text_reviews.append(review["text"])
    except KeyError:
        text_reviews = None
    
    place_info["name"] = place_name
    place_info["distance"] = distance
    place_info["duration"] = duration
    place_info["rating"] = rating
    place_info["location"] = location
    place_info["mode"] = mode
    place_reviews = text_reviews

    # json_object = json.dumps(places_info, indent=4)
    # with open("places-50-m.json", "w") as outfile:
    #     outfile.write(json_object)
    # json_object2 = json.dumps(places_reviews, indent=4)
    # with open("reviews-50-m.json", "w") as outfile:
    #     outfile.write(json_object2)

    return place_info, place_reviews