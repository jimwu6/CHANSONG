from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Api
import requests
import json

from . import services

app = Flask(__name__)
app.debug=True
CORS(app)
api = Api(app)

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def get():
    content = request.json
    print(request.json)
    
    model_name = request.args.get('model_name')
    input_text = request.args.get('input_text')
    length = request.args.get('length')
    temp = request.args.get('temperature')
    print(model_name)
    print(input_text)
    print(length)
    print(temp) 

    # return services.generate_lyrics("model_15_base", 0.9, 1000, '[Intro]')
    text = services.generate_lyrics(model_name, float(temp), int(length), input_text)
    print(repr(text))
    return text
