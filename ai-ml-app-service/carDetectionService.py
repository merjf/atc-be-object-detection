import pathlib
import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

class Model:
    def trainModel(self):
        data_dir = tf.keras.utils.get_file('cars', origin="./data/cars", untar=True)
        data_dir = pathlib.Path(data_dir)

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

        AUTOTUNE = tf.data.AUTOTUNE
        train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

        normalization_layer = layers.Rescaling(1./255)
        normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
        image_batch, labels_batch = next(iter(normalized_ds))
        first_image = image_batch[0]

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
        image_path = tf.keras.utils.get_file('Red_sunflower', origin=imageUrl)

        img = tf.keras.utils.load_img(
            image_path, target_size=(self.img_height, self.img_width)
        )
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch

        predictions = self.model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        return [self.class_names[np.argmax(score)], 100 * np.max(score)]