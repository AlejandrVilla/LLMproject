from dotenv import load_dotenv
load_dotenv('./env.txt')
from flask import Flask, request, json, jsonify
from flask_cors import CORS, cross_origin
import requests
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain_openai import ChatOpenAI
from gmaps_utils import (
    get_places, 
    get_geocode, 
    get_coord, 
    get_place_info
)
from langchain.chains import LLMChain, SimpleSequentialChain
import os
import json

from pprint import pprint

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# recomendation templates
recomendation_system_message = "You are a helpful assistant. You will receive some places with extra information: distances and times to get, ratings and comments."
recomendation_system_template = "You will give greater importance to the places by {order_by}"
recomendation_human_template_1 = "Prepare a plan to do an activity using one place for each type of activitie in the same order from the following list {places_info}, if there are no such place, print: \"no place availables for the activity\""
recomendation_human_template_2 = "Add the following summary of the reviews to your answer: {reviews_summary}"

recomendation_chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=recomendation_system_message),
        SystemMessagePromptTemplate.from_template(recomendation_system_template),
        HumanMessagePromptTemplate.from_template(recomendation_human_template_1),
        HumanMessagePromptTemplate.from_template(recomendation_human_template_2)
    ]
)

# get from summary reviews microservice
def get_summary_reviews(all_places_reviews):
    summary_reviews_url = "http://summary-reviews:5003/summary-reviews"
    # summary_reviews_url = "http://127.0.0.1:5003/summary_reviews"
    all_places_reviews = {"all_places_reviews": all_places_reviews}
    headers = {"Content-type": "application/json"}
    response = requests.post(summary_reviews_url, headers=headers, data=json.dumps(all_places_reviews))
    if response.status_code != 200:
        res = "Error trying to connect to summary reviews microservice"
        return 0, res
    res = response.json()
    reviews_summary = res["reviews_summary"]

    return 1, reviews_summary

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
    places_url = "http://extract-places:5002/extract-places"
    # places_url = "http://127.0.0.1:5002/extract_places"
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

# get response
def get_response(order_by, places_info, reviews_summary, temperature: float = 0.7):
    chat_openai = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature = temperature)

    recomendations_messages = recomendation_chat_prompt.format(
        order_by=order_by,
        places_info=places_info,
        reviews_summary=reviews_summary
    )

    response = chat_openai.invoke(recomendations_messages)
    return response

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

    reference_place = data.get('reference_place')
    order_by = data.get('order_by')
    origin = data.get('origin')
    radius = data.get('radius')
    mode = data.get('mode')
    language = data.get('language')
    temperature = data.get('temperature')

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
    reference_place_geocode = get_geocode(reference_place)
    reference_place_coord = get_coord(reference_place_geocode)
    origin_geocode = get_geocode(origin)
    origin_coord = get_coord(origin_geocode)
    all_places_info = {}
    all_places_reviews = {}

    for query_place in places_type:
        nearby_places, place_names, place_ids = get_places(
            query_place=query_place,
            coord=reference_place_coord,
            radius=radius,
            language=language
        )

        places_info, places_reviews = get_place_info(
            origin=origin_coord,
            place_names=place_names,
            place_ids=place_ids,
            mode=mode
        )
        all_places_info[query_place] = places_info
        all_places_reviews[query_place] = places_reviews

    # Save data
    # json_object2 = json.dumps(all_places_info, indent=4)
    # with open("all-places-50-m.json", "w") as outfile:
    #     outfile.write(json_object2)
    # json_object2 = json.dumps(all_places_reviews, indent=4)
    # with open("all-reviews-50-m.json", "w") as outfile:
    #     outfile.write(json_object2)
        
    # Get summary reviews from microservice
    # all_places_reviews = ""
    # all_places_info = ""
    error, reviews_summary = get_summary_reviews(
        all_places_reviews = all_places_reviews
    )
    if error == 0:
        # Format data
        res_dic = {"content": reviews_summary}
        # print(res_dic)
        response = jsonify(res_dic)
        response.status_code = 200
        return response

    # Get LLM response
    # reviews_summary = ""
    res = get_response(
        order_by=order_by,
        places_info=all_places_info,
        reviews_summary=reviews_summary,
        temperature=temperature
    )

    # Format data
    res_dict = {"content": res.content}
    
    print(res_dict)
    response = jsonify(res_dict)
    response.status_code = 200

    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)