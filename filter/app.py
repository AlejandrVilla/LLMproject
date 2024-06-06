from flask import Flask, jsonify, request
from transformers import DistilBertTokenizer
from transformers import TFDistilBertForSequenceClassification
from langchain.text_splitter import RecursiveCharacterTextSplitter as RC
import numpy as np

# load ai model
saved_model_path = "distilbert-filter"
tokenizer_v = DistilBertTokenizer.from_pretrained(saved_model_path)
model_v = TFDistilBertForSequenceClassification.from_pretrained(saved_model_path)

# text splitter ai model
text_splitter = RC(
    chunk_size=25,
    chunk_overlap=15,
    length_function=len
)

app = Flask(__name__)

@app.route('/filter', methods=["POST"])
def filter():
    content_type = request.headers.get("Content-type")
    if (content_type == "application/json"):
        data = request.json
        text = data.get("text")
        splitter_text = text_splitter.create_documents([text])
        predictions = {}
        for i in range(len(splitter_text)):
            # split text in tokens for the ai model input
            split_text = splitter_text[i].page_content
            # tolenize the text
            token = tokenizer_v(split_text, truncation=True, padding=True, return_tensors='tf')
            # prediction
            output = model_v(token)[0]
            # max value
            prediction = np.argmax(output, axis=1)
            # group text with prediction
            predictions[split_text] = prediction
            print(f"text: {split_text}")
            print(f"prediction: {prediction}")
            print()

        # print(predictions)
        if (1 or 0) in list(predictions.values()):
            pred = 0
        else:
            pred = 2
        res_dict = {"prediction": pred}
        response = jsonify(res_dict)
        response.status_code = 200
    else:
        message = {
            "status": 404,
            "message": "Content type us unsuported\n"
        }
        response = jsonify(message)
        response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004, debug=True)