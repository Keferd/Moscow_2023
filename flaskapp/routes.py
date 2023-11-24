import os

from flaskapp import app
import pandas as pd
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for, send_file
import functools
import json


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/api/text', methods=['POST'])
def post_text():
    try:
        text = request.form.get("text")
        
        if text:
            response_data = {
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