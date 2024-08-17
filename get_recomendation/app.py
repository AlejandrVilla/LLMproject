from dotenv import load_dotenv
load_dotenv('./env.txt')
from flask import Flask, request, json, jsonify
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
import requests
from gmaps_utils import (
    get_places, 
    get_geocode, 
    get_coord, 
    get_place_summary
)
import os
import json
import random
from pprint import pprint

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'alejandro'
app.config['MYSQL_DB'] = 'recomendation_app_db'
mysql = MySQL(app)

def get_filter_prediction(activities):
    filter_url = "http://filter:5004/filter"
    # filter_url = "http://127.0.0.1:5004/filter"
    text_dict = {
        "text": activities
    }
    header = {
        "Content-type": "application/json"
    }
    filter_response = requests.post(filter_url, headers=header, data=json.dumps(text_dict))
    if filter_response.status_code != 200:
        res = "Error trying to connect to filter microservice"
        return 0, res
    
    res = filter_response.json()
    prediction = res["prediction"]
    return 1, prediction

def get_extract_places(activities, language):
    # places_url = "http://extract-places:5002/extract-places"
    places_url = "http://127.0.0.1:5002/extract-places"
    activities_dict = {
        "activities": activities,
        "language": language
    }
    headers = {"Content-type": "application/json"}
    response = requests.post(places_url, headers=headers, data=json.dumps(activities_dict))
    if response.status_code != 200:
        res = "Error trying to connect extract places microservice"
        return 0, res
    
    res = response.json()
    places_type = res["places_type"]
    return 1, places_type

def post_group_places(group_places, places_type):
    # places_url = "http://get-plan:5005/post-plan"
    places_url = "http://127.0.0.1:5005/post-plan"
    group_places_dict = {
        "group_places": group_places,
        "places_type": places_type
    }
    headers = {"Content-type": "application/json"}
    response = requests.post(places_url, headers=headers, data=json.dumps(group_places_dict))
    if response.status_code != 200:
        res = "Error trying to connect post-plan method in get-plan microservice"
        return 0, res
    
    res = response.json()
    message = res["message"]
    return 1, message

# Microservice route
@app.route('/get-recomendation', methods=['POST'])
@cross_origin() # allow all origins all methods.
def get_recomendation():
    content_type = request.headers.get('Content-type')
    if (content_type != "application/json"):
        message = {
            "status": 404,
            "message": "Content type is unsuported\n"
        }
        response = jsonify(message)
        response.status_code = 404
        return response
    
    data = request.json
    activities = data.get('activities')
    # Extract information from url
    # error, prediction = get_filter_prediction(activities=activities)
    # if error == 0:
    #     # Format data
    #     res_dic = {"content": prediction}
    #     # print(res_dic)
    #     response = jsonify(res_dic)
    #     response.status_code = 200
    #     return response

    # if prediction != 2:
    #     content = "That is not a good prompt"
    #     res_dict = {"content": content}
    #     response = jsonify(res_dict)
    #     response.status_code = 200
    #     return response

    origin = data.get('origin')
    radius = data.get('radius')
    language = data.get('language')
    temperature = data.get('temperature')

    print("user data:")
    print(f"activities: {activities}")
    print(f"origin: {origin}")
    print(f"radius: {radius}")
    print(f"language: {language}")
    print(f"temperature: {temperature}")

    # Return activities from extract_places microservice
    error, places_type = get_extract_places(activities=activities, language=language)
    if error == 0:
        # Format data
        res_dic = {"content": places_type}
        # print(res_dic)
        response = jsonify(res_dic)
        response.status_code = 200
        return response

    # Using Google maps
    origin_geocode = get_geocode(origin)
    origin_coord = get_coord(origin_geocode)
    all_places_info = {}

    max_places = 0
    for query_place in places_type:
        nearby_places, place_names, place_ids = get_places(
            query_place=query_place,
            coord=origin_coord,
            radius=radius,
            language=language
        )
        places_info = []
        # max 3 elements
        for i in range(min(len(place_names), 3)):
            # Se puede extraer de la BD si ya existe
            cur = mysql.connection.cursor()
            cur.execute('''SELECT * FROM place WHERE place_id = %s''', (place_ids[i],))
            # tuple response
            data = cur.fetchall()
            cur.close()
            # read from database
            if len(data) != 0:
                data = list(data[0])
                place_id = place_ids[i]
                place_name = data[1]
                rating = data[2]
                phone_number = data[3]
                maps_url = data[4]
                place_info = {
                    "name": place_name,
                    "place_id": place_id,
                    "rating": rating,
                    "maps_url": maps_url,
                    "phone_number": phone_number,
                }
                print("fetched from database")
            # use google maps api
            else:
                place_info = get_place_summary(
                    place_name=place_names[i],
                    place_id=place_ids[i],
                )
                # Insert into data base
                cur = mysql.connection.cursor()
                cur.execute(
                    '''
                    INSERT INTO place (place_id, placename, rating, phone, maps_url)
                    VALUES(%s, %s, %s, %s, %s)
                    ''', 
                    (
                        place_info['place_id'],
                        place_info['name'],
                        place_info['rating'],
                        place_info['phone_number'],
                        place_info['maps_url']
                    )
                )
                mysql.connection.commit()
                cur.close()
                print(f"insert place: {place_info['name']}")
            places_info.append(place_info)
        all_places_info[query_place] = places_info
        if(len(places_info) > max_places):
            max_places = len(places_info)

    # Save data
    json_object = json.dumps(all_places_info, indent=4)
    with open("places_info.json", "w") as outfile:
        outfile.write(json_object)

    group_places = []
    # max 3 groups recomendations
    for i in range(min(3, max_places)):
        places = []
        # for each place extract one place randomly
        for query_place in places_type:
            place = {}
            if(len(all_places_info[query_place]) == 0):
                place = {"type": query_place}
            else:
                ind = random.randint(0, len(all_places_info[query_place])-1)
                place = all_places_info[query_place][ind]
                place["type"] = query_place
            places.append(place)
        group_places.append(places)

    # with open('group_places.json', 'r') as file:
    #     group_places = json.load(file)
    # with open('places_type.json', 'r') as file:
    #     places_type = json.load(file)

    # Return activities from extract_places microservice
    error, message = post_group_places(
        group_places=group_places, 
        places_type=places_type
    )
    if error == 0:
        # Format data
        res_dict = {"content": message}
        # print(res_dict)
        response = jsonify(res_dict)
        response.status_code = 200
        return response
    print(message)

    # Format data
    res_dict = {"content": group_places}
    
    json_object = json.dumps(group_places, indent=4)
    with open("group_places.json", "w") as outfile:
        outfile.write(json_object)
    json_object = json.dumps(places_type, indent=4)
    with open("places_type.json", "w") as outfile:
        outfile.write(json_object)
    
    # print(res_dict)
    response = jsonify(res_dict)
    response.status_code = 200

    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)