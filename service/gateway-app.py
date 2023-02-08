from flask import Flask, jsonify, request, flash, request, redirect
from flask_cors import CORS, cross_origin
from PIL import Image
from werkzeug.utils import secure_filename
import os
import car_cetection_service as ccs

app = Flask(__name__)
model = ccs.Model()
CORS(app, expose_headers='Authorization')

@app.route("/test-image", methods=['POST', 'GET'])
def uploadImage():
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
        [className, accuracy] = model.testModel("./data/test/test.jpg")
        response = {
            'accuracy': accuracy,
            'class': className
        }
        return jsonify(response)
    response = {
        'message': "Something went wrong!",
        'code': 500
    }
    return jsonify(response)

@app.route("/test-car-model", methods=['POST'])
def testModel():
    if request.method == 'POST':
        print(request)
        # [className, accuracy] = model.testModel("./data/test/test.jpg")
        response = {
            'accuracy': 10,
            'class': 'className',
            'message': 200
        }
        return jsonify(response)
    response = {
        'message': "Something went wrong!",
        'code': 500
    }
    return jsonify(response)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)
