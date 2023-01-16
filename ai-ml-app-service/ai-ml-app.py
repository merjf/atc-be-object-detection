from flask import Flask, jsonify
from flask_cors import CORS
import os

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

if __name__ == "ai-ml-app ":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)