from dotenv import load_dotenv
load_dotenv('./env.txt')
from flask import Flask, request, json, jsonify
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import (
    SystemMessage,
)
from langchain_openai import ChatOpenAI

# summary reviews templates
summary_system_message = "You will receive a list of place reviews in a json format, generate a summary for each place in the same format. Put in your answer only the summary"
summary_human_template = "{all_places_reviews}"

summary_chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=summary_system_message),
        HumanMessagePromptTemplate.from_template(summary_human_template)
    ]
)

app = Flask(__name__)

# Summary of all reviews
@app.route('/summary_reviews', methods=["POST"])
def summary_reviews():
    content_type = request.headers.get('Content-type')
    if (content_type == "application/json"):
        data = request.json
        # all_places_reviews -> dict
        all_places_reviews = data.get('all_places_reviews')
        
        chat_openai = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature = 0.7)
        # summary reviews
        reviews_messages = summary_chat_prompt.format(
            all_places_reviews=all_places_reviews
        )
        reviews_summary = chat_openai.invoke(reviews_messages)
        
        # Format data
        # reviews_summary.content -> str
        res_dict = {"reviews_summary": reviews_summary.content}
        response = jsonify(res_dict)
        response.status_code = 200
    else:
        message = {
            "status": 404,
            "message": "Content type is insuported\n"
        }
        response = jsonify(message)
        response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)