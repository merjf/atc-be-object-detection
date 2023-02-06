import pathlib
import numpy as np
from flask import Flask, jsonify, request, flash, request, redirect

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

class Model:
    def __init__(self):
        data_dir = pathlib.Path("./data/cars/")

        batch_size = 32
        self.img_height = 180
        self.img_width = 180
        
        train_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(self.img_height, self.img_width),
            batch_size=batch_size)
        val_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(self.img_height, self.img_width),
            batch_size=batch_size)
        self.class_names = train_ds.class_names

        num_classes = len(self.class_names)

        self.model = Sequential([
            layers.Rescaling(1./255, input_shape=(self.img_height, self.img_width, 3)),
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
        
        self.model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
        
        epochs=10
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs
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

        epochs = 20
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs
        )

    def testModel(self, imageUrl):
        img = tf.keras.utils.load_img(
            imageUrl, target_size=(self.img_height, self.img_width)
        )
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        predictions = self.model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        return [self.class_names[np.argmax(score)], 100 * np.max(score)]

app = Flask(__name__)
app.debug = True
model = Model()

@app.route("/car-dataset-info", methods=['GET'])
def getCarDatasetInfo():
    [className, accuracy] = model.testModel("./data/test/test.jpg")
    response = {
        'accuracy': accuracy,
        'class': className
    }
    return jsonify(response)