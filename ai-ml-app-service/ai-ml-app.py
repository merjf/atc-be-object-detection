from flask import Flask, jsonify, request, flash, request, redirect
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

CORS(app, expose_headers='Authorization')

@app.route("/upload-image", methods=['POST', 'GET'])
def uploadImage():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        response = {
            'value': [1, 2, 3],
            'message': "Image uploaded successfully: " + filename
        }
        return jsonify(response)
    response = {
        'value': [1, 2, 3],
        'message': "Something went wrong!"
    }
    return jsonify(response)

@app.route("/car-dataset-info", methods=['GET'])
def getCarDatasetInfo():
    response = {
        'value': [1, 2, 3],
        'message': "Something went wrong!"
    }
    return jsonify(response)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)