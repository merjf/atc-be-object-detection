import pathlib
import numpy as np
import os
from flask import Flask, jsonify, request, flash, request, redirect
import PIL

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

CAR_DATASET_PATH = "./data/cars/"
CHECKPOINT_DIR = "model/checkpoints/"
CHECKPOINT_PATH = "model/checkpoints/cp-{epoch:04d}.ckpt"

class Model:
    def __init__(self):
        if os.path.exists(CHECKPOINT_PATH):
            os.listdir(CHECKPOINT_PATH)
            latest = tf.train.latest_checkpoint(CHECKPOINT_DIR)
            [self.model, train_ds, val_ds, num_classes] = self.createModel()
            self.model.load_weights(latest)
        else: 
            [self.model, train_ds, val_ds, num_classes] = self.createModel()
            cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=CHECKPOINT_PATH, save_weights_only=True, verbose=1)

            epochs = 20
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

            epochs = 40
            history = self.model.fit(
                train_ds,
                validation_data=val_ds,
                epochs=epochs,
                callbacks=[cp_callback]
            )
            self.model.save_weights(CHECKPOINT_PATH.format(epoch=60))

    def testModel(self, imageUrl):
        img = tf.keras.utils.load_img(
            imageUrl, target_size=(self.img_height, self.img_width)
        )
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        predictions = self.model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        return [self.class_names[np.argmax(score)], 100 * np.max(score)]
    
    def createModel(self):
        data_dir = pathlib.Path(CAR_DATASET_PATH)

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

        model = Sequential([
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
        
        model.compile(optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])

        return [model, train_ds, val_ds, num_classes]