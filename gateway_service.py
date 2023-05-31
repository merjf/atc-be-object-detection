import os
import json
from telnetlib import IP
from PIL import Image
from flask import Flask, jsonify, request, flash, request, redirect
from flask_cors import CORS, cross_origin
from model import Model

app = Flask(__name__)
model = Model()
CORS(app, expose_headers='Authorization')

@app.route("/select-dataset", methods=['GET'])
def selectDataset():
    response = {
        'dataset': 'cars_1',
        'message': 'ok'
    }
    return jsonify(response)

@app.route("/test-model", methods=['POST'])
def testModel():
    predictions = []
    message = "error"
    response = {
        'predictions': predictions,
        'message': message
    }
    if request.method == 'POST':
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
        if(img):
            message = "ok"
            predictions = model.testModel("./data/test/test.jpg")
        response = {
            'predictions': predictions,
            'message': message
        }
        return jsonify(response)
    return jsonify(response)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="127.0.0.1", port=5003, use_reloader=False)