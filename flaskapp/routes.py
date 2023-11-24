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

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

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

        if text:
            response_data = {
                'image_url': image_base64,
                'executor': "Лысьвенский городской округ", 
                'group': "Благоустройство",
                'subject': "★ Ямы во дворах"
            }

            return jsonify(response_data)
        else:
            return "Отсутствует текст", 400
    except Exception as e:
        print(e)
        return str(e), 500

def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))


def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)