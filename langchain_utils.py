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

system_message = "You will receive a list of place reviews in a json format, generate a summary for each place in the same format"
human_template = "{places_reviews}"

chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=system_message),
        HumanMessagePromptTemplate.from_template(human_template)
    ]
)

system_message_2 = "You are a helpful assistant"
# system_message_2 = "You will receive some places, distances and times to get. You will list the places in ascendent order by ratings and arrival time"
system_template = "You will receive some places with extra information: distances and times to get, ratings and comments. You will list the places in ascendent order by {order_by}"
human_template_2 = "Give me the best {n_places} nearest places to get from the following list {places_info}"
human_template_3 = "Add the following summary of the reviews to your answer: {reviews_summary}"

chat_prompt_2 = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=system_message_2),
        # SystemMessage(content=system_message_2),
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template_2),
        HumanMessagePromptTemplate.from_template(human_template_3)
    ]
)


def get_response(order_by, places_info, places_reviews, n_places: int = 5, temperature: float = 0.7):
    chat_openai = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature = temperature)

    messages = chat_prompt.format(
        places_reviews=places_reviews
    )
    # pprint(messages)
    reviews_summary = chat_openai.invoke(messages)
    # print(reviews_summary.content)

    messages2 = chat_prompt_2.format(
        order_by=order_by,
        n_places=n_places,
        places_info=places_info,
        reviews_summary=reviews_summary.content
    )
    # pprint(messages2)

    response = chat_openai.invoke(messages2)
    return response

def get_recomendation(reference_place, order_by, origin, query_place, radius, mode, language, n_places, temperature):
    geocode = get_geocode(reference_place)
    coord = get_coord(geocode)
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

    response = get_response(
        order_by=order_by,
        places_info=places_info,
        places_reviews=places_reviews,
        n_places=n_places,
        temperature=temperature
    )
    # print(response.content)
    return response