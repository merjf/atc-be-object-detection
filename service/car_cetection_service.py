import pathlib
import re
import os
import numpy as np
from telnetlib import IP
from PIL import Image
from flask import Flask, jsonify, request, flash, request, redirect
from flask_cors import CORS, cross_origin
import util
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

CAR_DATASET_PATH = "./data/cars/"
CHECKPOINT_PATH = "model/checkpoints/cp-{epoch:04d}.ckpt"
CHECKPOINT_DIR = os.path.dirname(CHECKPOINT_PATH)

BATCH_SIZE = 32
IMG_HEIGHT = 180
IMG_WIDTH = 180
EPOCHS = 20

class Model:
    def __init__(self):
        print("init")
        if os.path.exists(CHECKPOINT_DIR):
            latest = tf.train.latest_checkpoint(CHECKPOINT_DIR)
            currentCheckpoint = int(re.search(r'\d+', latest).group())
            if(currentCheckpoint == EPOCHS):
                self.createModel()
                self.model.load_weights(latest)
            # else:
            #     [self.model, train_ds, val_ds, num_classes] = self.createModel()
            #     self.model.load_weights(latest)
            #     self.trainModel(train_ds, val_ds, num_classes, currentCheckpoint)
        # else: 
        #     [self.model, train_ds, val_ds, num_classes] = self.createModel()
        #     self.trainModel(train_ds, val_ds, num_classes)
            
    def createModel(self):
        print("create")
        data_dir = pathlib.Path(CAR_DATASET_PATH)
        
        train_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(IMG_HEIGHT, IMG_WIDTH),
            batch_size=BATCH_SIZE)
        val_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(IMG_HEIGHT, IMG_WIDTH),
            batch_size=BATCH_SIZE)
        self.class_names = train_ds.class_names

        num_classes = len(self.class_names)

        model = Sequential([
            layers.Rescaling(1./255, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(num_classes)
        ])
        
        model.compile(optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])

        return [model, train_ds, val_ds, num_classes]

    def trainModel(self, train_ds, val_ds, num_classes, currentCheckpoint=0):
        print("train")
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=CHECKPOINT_PATH, save_weights_only=True, verbose=1,save_freq=2*BATCH_SIZE)

        epochs = EPOCHS - currentCheckpoint
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=[cp_callback]
        )

        data_augmentation = keras.Sequential([
            layers.RandomFlip("horizontal", input_shape=(self.img_height, self.img_width, 3)),
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1),
        ])

        self.model = Sequential([
            data_augmentation,
            layers.Rescaling(1./255),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Dropout(0.2),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(num_classes, name="outputs")
        ])

        self.model.compile(optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])

        epochs = EPOCHS * 2 - currentCheckpoint
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=[cp_callback]
        )
        self.model.save_weights(CHECKPOINT_PATH.format(epoch=60))

    def testModel(self, imageUrl):
        print(imageUrl)
        img = tf.keras.utils.load_img(
            imageUrl, target_size=(IMG_HEIGHT, IMG_WIDTH)
        )
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        predictions = self.model.predict(img_array)
        values = []
        for prediction in predictions:
            score = tf.nn.softmax(prediction)
            values.append({
                "accuracy": 100 * np.max(score),
                "class": self.class_names[np.argmax(score)]
            }) 
        return values

app = Flask(__name__)
carModel = Model()
CORS(app, expose_headers='Authorization')

@app.route("/test-model", methods=['GET'])
def testModel():
    response = {}
    image = request.args.get("image_url")
    if(image):    
        [classes, predictions] = carModel.testModel("./data/test/test.jpg")
        response = {
            'predictions': predictions,
            'classes': classes
        }
    else:
        response = {
            'message': 'error'
        }
    return jsonify(response)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, host=util.IP, port=util.CAR_DETECTION_SERVICE_PORT, use_reloader=False)