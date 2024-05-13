from dotenv import load_dotenv
load_dotenv('./env.txt')
from flask import Flask, request, json, jsonify
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

# recomendation templates
recomendation_system_message = "You are a helpful assistant. You will receive some places with extra information: distances and times to get, ratings and comments."
recomendation_system_template = "You will give greater importance to the places by {order_by}"
recomendation_human_template_1 = "Give me a plan to do an activity using one place for each type of place in the same order from the following list {places_info}, if there are no such place, print \"no place availables for the activity\""
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
    summary_reviews_url = "http://summary_reviews:5003/summary_reviews"
    all_places_reviews = {"all_places_reviews": all_places_reviews}
    headers = {"Content-type": "application/json"}
    response = requests.post(summary_reviews_url, headers=headers, data=json.dumps(all_places_reviews))
    if response.status_code == 200:
        res = response.json()
        reviews_summary = res["reviews_summary"]
    else:
        reviews_summary = None

    return reviews_summary

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
@app.route('/get_recomendation', methods=['POST'])
def get_recomendation():
    content_type = request.headers.get('Content-type')
    if (content_type == "application/json"):
        data = request.json
        # Extract information from url
        reference_place = data.get('reference_place')
        order_by = data.get('order_by')
        origin = data.get('origin')
        activities = data.get('activities')
        radius = data.get('radius')
        mode = data.get('mode')
        language = data.get('language')
        temperature = data.get('temperature')

        # Return activities from extract_places microservice
        places_url = "http://extract_places:5002/extract_places"
        activities_dict = {
            "activities": activities,
            "language": language
        }
        headers = {"Content-type": "application/json"}
        response = requests.post(places_url, headers=headers, data=json.dumps(activities_dict))
        if response.status_code == 200:
            res = response.json()
            places_type = res["places_type"]
        else:
            places_type = None
        
        # Using Google maps
        geocode = get_geocode(reference_place)
        coord = get_coord(geocode)
        all_places_info = {}
        all_places_reviews = {}

        for query_place in places_type:
            nearby_places, place_names, place_ids = get_places(
                query_place=query_place,
                coord=coord,
                radius=radius,
                language=language
            )

            places_info, places_reviews = get_place_info(
                origin=origin,
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
        reviews_summary = get_summary_reviews(
            all_places_reviews = all_places_reviews
        )

        # Get LLM response
        res = get_response(
            order_by=order_by,
            places_info=all_places_info,
            reviews_summary=reviews_summary,
            temperature=temperature
        )

        # Format data
        res_dic = {"content": res.content}
        # print(res_dic)
        response = jsonify(res_dic)
        response.status_code = 200
    else:
        message = {
            "status": 404,
            "message": "Content type is insuported\n"
        }
        response = jsonify(message)
        response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)