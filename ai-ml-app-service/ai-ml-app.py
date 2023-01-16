from flask import Flask, jsonify
from flask_cors import CORS

print('#######################')
print('Service AI & ML Started')
print('#######################')

app = Flask(__name__)
CORS(app)

@app.route("/result", methods=['GET'])
def getResult():
    response = {
        'value': [1, 2, 3],
        'message': "200 OK"
    }
    return jsonify(response)

@app.route("/upload-image", methods=['POST'])
def uploadImage():
    return 'Hi'