import os
import numpy as np
from PIL import Image
import requests
from flask import Flask, jsonify, request, flash, redirect
from flask_cors import CORS
import util

import util

app = Flask("__main__")
CORS(app, expose_headers='Authorization')

@app.route("/test-car-model", methods=['POST'])
def uploadImage():
    if request.method == 'POST':
        print("dsanodsao")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        img = Image.open(file)
        img = img.convert('L')
        img.save('./data/test/test.jpg')
        print(type(util.IP))
        url = "http://"+util.IP+":"+str(util.CAR_DETECTION_SERVICE_PORT)+"/test-model"
        params = {'image_url': './data/test/test.jpg'}
        response = requests.get(url = url, params = params)
        print(response.json())
        predictions = requests.get(url)
        response = {
            'predictions': predictions
        }
        return jsonify(response)
    response = {
        'message': "Something went wrong!",
        'code': 500
    }
    return jsonify(response)

@app.route("/car-dataset-info", methods=['GET'])
def getCarDatasetInfo():
    response = {
        'accuracy': 10,
        'class': 'className',
        'message': 200
    }
    return jsonify(response)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, host=util.IP, port=util.GATEWAY_PORT, use_reloader=False)
