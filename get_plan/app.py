from dotenv import load_dotenv
load_dotenv('./env.txt')
from flask import Flask, request, json, jsonify
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
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
    get_place_info,
    get_place_summary
)
from langchain.chains import LLMChain, SimpleSequentialChain
import os
import json
import random
from uuid import uuid4
from pprint import pprint

sql_user = os.environ['MYSQL_USER']
sql_pw = os.environ['MYSQL_PASSWORD']

app = Flask(__name__)
CORS(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = sql_user
app.config['MYSQL_PASSWORD'] = sql_pw
app.config['MYSQL_DB'] = 'recomendation_app_db'
mysql = MySQL(app)

# recomendation templates
recomendation_system_message = "You are a helpful assistant. You will receive some places with extra information: distances and times to get, ratings and comments."
recomendation_system_template = "Make a {plan_type} plan, Do not use any format in your answer"
recomendation_human_template_1 = "Give a plan using the places from the following list {places_info}, if there are no such place, print: \"no place availables for the activity\""
recomendation_human_message = "Add to your answers a summary of the reviews"

recomendation_chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=recomendation_system_message),
        SystemMessagePromptTemplate.from_template(recomendation_system_template),
        HumanMessagePromptTemplate.from_template(recomendation_human_template_1),
        HumanMessage(recomendation_human_message)
    ]
)

# get from summary reviews microservice
def get_summary_reviews(place_reviews):
    # summary_reviews_url = "http://summary-reviews:5003/summary-reviews"
    summary_reviews_url = "http://127.0.0.1:5003/summary-reviews"
    place_reviews = {"place_reviews": place_reviews}
    headers = {"Content-type": "application/json"}
    response = requests.post(summary_reviews_url, headers=headers, data=json.dumps(place_reviews))
    if response.status_code != 200:
        res = "Error trying to connect to summary reviews microservice"
        return 0, res
    res = response.json()
    reviews_summary = res["reviews_summary"]

    return 1, reviews_summary

# Connect to filter microservice
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

# get response from LLM
def get_response(places_info, plan_type, temperature: float = 0.7):
    # chat_openai = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature = temperature)
    chat_openai = ChatOpenAI(model="gpt-4o", temperature = temperature)

    recomendations_messages = recomendation_chat_prompt.format(
        plan_type=plan_type,
        places_info=places_info,
    )

    response = chat_openai.invoke(recomendations_messages)
    return response

# global group_places
# global places_type

# Get group places as plans from get recomendation microservice
@app.route('/post-plan', methods=['POST'])
@cross_origin() # allow all origins all methods.
def post_plan():
    global prompt
    global group_places
    global places_type
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
    prompt = data.get('prompt')
    group_places = data.get('group_places')
    places_type = data.get('places_type')

    json_object = json.dumps(group_places, indent=4)
    with open("group_places.json", "w") as outfile:
        outfile.write(json_object)
    json_object = json.dumps(places_type, indent=4)
    with open("places_type.json", "w") as outfile:
        outfile.write(json_object)

    message = {
        "message": "groups loaded"
    }
    print(message["message"])
    # print(group_places)
    response = jsonify(message)
    response.status_code = 200
    return response

# Microservice route
@app.route('/get-plan', methods=['POST'])
@cross_origin() # allow all origins all methods.
def get_plan():
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
    ind = int(data.get('ind'))
    plan_type = data.get('plan_type')
    origin = data.get('origin')
    mode = data.get('mode')
    temperature = data.get('temperature')
    user_id = data.get("user_id")

    print("user data:")
    print(f"user: {user_id}")
    print(f"origin: {origin}")
    print(f"mode: {mode}")
    print(f"plan_type: {plan_type}")
    print(f"temperature: {temperature}")

    print(f"index plan: {ind}")
    print(group_places[ind])
    places = group_places[ind]

    json_object = json.dumps(places, indent=4)
    with open("places.json", "w") as outfile:
        outfile.write(json_object)

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

    # Using Google maps
    origin_geocode = get_geocode(origin)
    origin_coord = get_coord(origin_geocode)
    all_places_info = []
    all_places_info2 = []

    for place in places:
        if "name" in place:
            place_name = place["name"]
            place_id = place["place_id"]
            rating = place["rating"]
            maps_url = place["maps_url"]
            phone_number = place["phone_number"]
            # opened = place["opened"]
            type = place["type"]

            place_info, place_reviews = get_place_info(
                origin = origin_coord,
                place_name = place_name,
                place_id = place_id,
                mode = mode
            )
        
            # Get summary reviews from microservice
            # all_places_reviews = ""
            # all_places_info = ""
            error, summary_review = get_summary_reviews(
                place_reviews = place_reviews
            )
            if error == 0:
                # Format data
                res_dic = {"content": summary_review}
                # print(res_dic)
                response = jsonify(res_dic)
                response.status_code = 200
                return response
        
            place_info["summary_review"] = summary_review
            all_places_info.append(place_info)
            place_tmp = place_info.copy()
            place_tmp["place_id"] = place_id
            place_tmp["phone_number"] = phone_number
            # place_tmp["opened"] = opened
            place_tmp["maps_url"] = maps_url
            place_tmp["type"] = type
            all_places_info2.append(place_tmp)

    # print(all_places_info)
    json_object = json.dumps(all_places_info, indent=4)
    with open("all_places_info.json", "w") as outfile:
        outfile.write(json_object)

    # Get LLM response
    # reviews_summary = ""
    res = get_response(
        places_info = all_places_info,
        plan_type = plan_type,
        temperature = temperature
    )

    # save in prompt table
    prompt_id = uuid4().hex
    cur = mysql.connection.cursor()
    cur.execute(
        '''
        INSERT INTO prompt (prompt_id, prompt_text, user_id)
        VALUES (%s, %s, %s)
        ''',
        (prompt_id, prompt, user_id)
    )
    cur.connection.commit()
    print(f"prompt: {prompt_id} asked by user: {user_id} inserted in db")
    # save in answer table
    answer_id = uuid4().hex
    cur.execute(
        '''
        INSERT INTO answer (answer_id, answer_text, prompt_id)
        VALUES (%s, %s, %s)
        ''',
        (answer_id, res.content, prompt_id)
    )
    cur.connection.commit()
    cur.close()
    print(f"answer: {answer_id} for the user: {user_id} inserted in db")

    # Format data
    res_dict = {
        "content": res.content,
        "places_info": all_places_info2
    }
    
    json_object = json.dumps(res_dict, indent=4)
    with open("model_answer.json", "w") as outfile:
        outfile.write(json_object)
    
    print("answer sended")
    print(res_dict)
    response = jsonify(res_dict)
    response.status_code = 200

    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)