import os

from flaskapp import app
import pandas as pd
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for, send_file
import functools
import json

from wordcloud import WordCloud
import matplotlib.pyplot as plt

import base64
from io import BytesIO

from flaskapp.utils import get_frontend_table

from flaskapp.ml.catboost.performer_classifier import performer_classifier
from flaskapp.ml.inference import predict_group, predict_theme
from preprocessing import soft_remove
from spell_and_summarization import spell_txt, summarization_txt
from ner import extract_addresses

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/table')
def table():
    return render_template('table.html')

@app.route('/api/text', methods=['POST'])
def post_text():
    try:
        text = request.form.get("text")
        
        word_cloud_text = ' '.join((text.split()))
        wordcloud = WordCloud(
            max_font_size=100,
            max_words=100,
            background_color= "#fff",
            scale=10,
            width=400,
            height=400
        ).generate(word_cloud_text)
        plt.figure(figsize=(10,10))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        # plt.close()


        text = soft_remove(text)
        predicted_group = predict_group(text)
        predicted_topic = predict_theme(text=text, predicted_group=predicted_group)
        predicted_spell = spell_txt(text)
        predicted_summarization = summarization_txt(text)
        predicted_loc = extract_addresses(text)
        predicted_executor = performer_classifier(predicted_group, predicted_topic)

        # predicted_group = predict_group(text)
        # predicted_topic = predict_theme(text=text, predicted_group=predicted_group)
        # predicted_executor = "___"
        # predicted_spell = spell_txt(soft_remove(text))
        # predicted_summarization = summarization_txt(soft_remove(text))
        # predicted_loc = extract_addresses(text)

        if text:
            response_data = {
                'image_url': image_base64,
                'executor': predicted_executor, 
                'group': predicted_group,
                'topic': predicted_topic,
                'spell': predicted_spell,
                'summarization': predicted_summarization,
                'loc': predicted_loc
            }

            return jsonify(response_data)
        else:
            return "Отсутствует текст", 400
    except Exception as e:
        print(e)
        return str(e), 500

@app.route('/api/table', methods=['POST'])
def post_table():
    file = request.files["file"]

    if file and file.filename.endswith('.csv'):
        try:
            csv_data = pd.read_csv(file, delimiter=';')
            csv_data.columns = ['executor', 'group', 'text', 'subject']

            text = pd.DataFrame(csv_data['text'])
            front_table = get_frontend_table(text)

            print(front_table.columns)
            print(front_table)

            data = front_table.to_dict(orient='records')
            n = len(front_table.columns)

            json_data = json.dumps(data, indent=n)

            return json_data
        except Exception as e:
            print("error:", e)
            return str(e), 500
    else:
        return "Файл должен быть формата .csv", 400

def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))


def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)