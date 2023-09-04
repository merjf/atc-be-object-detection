# from flask import Blueprint, Flask, jsonify, request, flash, request, redirect
# import model
# from util import getPreviewImage
# from PIL import Image

# all_routes = Blueprint('atc-be-object-detection', __name__)

# @all_routes.route("/load-dataset", methods=['GET'])
# def selectDataset():
#     dataset = request.args.get('dataset')
#     message = 'Dataset not found'
#     image = []
#     classes = []
#     if(dataset):
#         model.model = model.Model(dataset)
#         message = ('Dataset loaded: '+ dataset)
#         image = getPreviewImage(dataset)
#         classes = model.model.labelClasses
#     print(classes)
#     response = {
#         'dataset': {
#             'name': dataset.replace("_", " ").capitalize(),
#             'id': dataset,
#             'image': str(image),
#             'classes': classes
#         },
#         'message': message
#     }
#     return jsonify(response)

# @all_routes.route("/test-model", methods=['POST'])
# def testModel():
#     if(model.model):
#         predictions = []
#         message = "error"
#         response = {
#             'predictions': predictions,
#             'message': message
#         }
#         if request.method == 'POST':
#             if 'file' not in request.files:
#                 flash('No file part')
#                 return redirect(request.url)
#             file = request.files['file']
#             if file.filename == '':
#                 flash('No selected file')
#                 return redirect(request.url)
#             img = Image.open(file)
#             img = img.convert('L')
#             img.save('./data/test/test.jpg')
#             if(img):
#                 message = "ok"
#                 predictions = model.model.testModel("./data/test/test.jpg")
#             response = {
#                 'predictions': predictions,
#                 'message': message
#             }
#             return jsonify(response)
#     response = {
#         'predictions': [],
#         'message': 'Dataset not loaded'
#     }
#     return jsonify(response)