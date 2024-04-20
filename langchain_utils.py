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

# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# summary reviews templates
summary_system_message = "You will receive a list of place reviews in a json format, generate a summary for each place in the same format. Put in your answer only the summary"
summary_human_template = "{places_reviews}"

summary_chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=summary_system_message),
        HumanMessagePromptTemplate.from_template(summary_human_template)
    ]
)

# recomendation templates
recomendation_system_message = "You are a helpful assistant. You will receive some places with extra information: distances and times to get, ratings and comments."
recomendation_system_template = "You will give greater importance to the places by {order_by}"
recomendation_human_template_1 = "Give me a plan to do an activity using one place for each type of place from the following list {places_info}"
recomendation_human_template_2 = "Add the following summary of the reviews to your answer: {reviews_summary}"

recomendation_chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=recomendation_system_message),
        SystemMessagePromptTemplate.from_template(recomendation_system_template),
        HumanMessagePromptTemplate.from_template(recomendation_human_template_1),
        HumanMessagePromptTemplate.from_template(recomendation_human_template_2)
    ]
)

# activities templates
activities_system_message = "You will receive a plan from a user to do some activities and you have to extract only places as a python list"
activities_human_template = "{activities}"

activities_chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content = activities_system_message),
        HumanMessagePromptTemplate.from_template(activities_human_template)
    ]
)

def extract_places(activities):
    chat_openai = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature = 0.7)
    activities_messages = activities_chat_prompt.format(
        activities=activities
    )
    places_type = chat_openai.invoke(activities_messages)
    places_type = eval(places_type.content)
    return places_type


def get_response(order_by, places_info, places_reviews, temperature: float = 0.7):
    chat_openai = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature = temperature)

    # summary reviews
    reviews_messages = summary_chat_prompt.format(
        places_reviews=places_reviews
    )
    reviews_summary = chat_openai.invoke(reviews_messages)

    # get recomendations
    recomendations_messages = recomendation_chat_prompt.format(
        order_by=order_by,
        places_info=places_info,
        reviews_summary=reviews_summary.content
    )

    response = chat_openai.invoke(recomendations_messages)
    return response

def get_recomendation(reference_place, order_by, origin, activities, radius, mode, language, temperature):
    geocode = get_geocode(reference_place)
    coord = get_coord(geocode)

    # return query_places for each place
    places_type = extract_places(activities=activities)
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

    json_object2 = json.dumps(all_places_info, indent=4)
    with open("all-places-50-m.json", "w") as outfile:
        outfile.write(json_object2)
    json_object2 = json.dumps(all_places_reviews, indent=4)
    with open("all-reviews-50-m.json", "w") as outfile:
        outfile.write(json_object2)
        
    response = get_response(
        order_by=order_by,
        places_info=all_places_info,
        places_reviews=all_places_reviews,
        temperature=temperature
    )
    return response