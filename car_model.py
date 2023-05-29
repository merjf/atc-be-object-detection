import pathlib
import re
import os
import numpy as np
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
EPOCHS = 3

class Model:
    def __init__(self):
        print("init model")
        if os.path.exists(CHECKPOINT_DIR):
            latest = tf.train.latest_checkpoint(CHECKPOINT_DIR)
            currentCheckpoint = int(re.search(r'\d+', latest).group())
            if(currentCheckpoint == EPOCHS):
                [self.model, train_ds, val_ds, num_classes] = self.createModel("load model")
                self.model.load_weights(latest)
            else:
                [self.model, train_ds, val_ds, num_classes] = self.createModel("create model")
                self.model.load_weights(latest)
                self.trainModel(train_ds, val_ds, num_classes, currentCheckpoint)
        else: 
            [self.model, train_ds, val_ds, num_classes] = self.createModel()
            self.trainModel(train_ds, val_ds, num_classes)
            
    def createModel(self, debug):
        print(debug)
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
        print("train model")
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=CHECKPOINT_PATH, save_weights_only=True, verbose=1,save_freq=2*BATCH_SIZE)

        epochs = EPOCHS - currentCheckpoint
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=[cp_callback]
        )

    def testModel(self, imageUrl):
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
                "classes": self.class_names[np.argmax(score)]
            })
        return values