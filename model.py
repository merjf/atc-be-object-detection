import pathlib
import json
import os
from ast import literal_eval
import tensorflow as tf
from tensorflow import keras
import h5py

BATCH_SIZE = 32
IMG_HEIGHT = 180
IMG_WIDTH = 180
EPOCHS = 10
EPOCHS_DATA_AUG = 20
AUTOTUNE = tf.data.AUTOTUNE

class Settings:
    def __init__(self, dataset):
        self.DATASET = dataset
        self.DATASET_PATH = "./data/"+self.DATASET+"/"
        self.CHECKPOINT_PATH = "./model_checkpoints/"+self.DATASET+"/cp-{epoch:04d}.ckpt"
        self.CHECKPOINT_DIR = os.path.dirname(self.CHECKPOINT_PATH)
    def getCheckpointDir(self):
        return self.CHECKPOINT_DIR
    def getCheckpointPath(self):
        return self.CHECKPOINT_PATH
    def getDatasetPath(self):
        return self.DATASET_PATH

class Model:
    def __init__(self, dataset):
        settings = Settings(dataset)
        print("Init Model - Dataset: ", dataset)
        if os.path.exists(settings.getCheckpointDir()+"/model.h5"):
            self.model, self.labelClasses = self.loadModel(settings)
        else: 
            [self.model, train_ds, val_ds, class_names] = self.createModel(settings)
            latest = tf.train.latest_checkpoint(settings.getCheckpointDir())
            if os.path.exists(settings.getCheckpointDir()+"/model") and latest:
                self.model.load_weights(latest)
            else:
                [self.model, train_ds, val_ds, class_names] = self.createModel(settings)
            self.trainModel(train_ds, val_ds, class_names, settings)
            self.trainModelWithDataAugmentation(train_ds, val_ds, class_names, settings)

    def loadModel(self, settings):
        print("Load Model")
        self.model = tf.keras.models.load_model(settings.getCheckpointDir()+"/model.h5")
        latest = tf.train.latest_checkpoint(settings.getCheckpointDir())
        self.model.load_weights(latest)
        modelFile = h5py.File(settings.getCheckpointDir()+"/model.h5", mode='r')
        labelClasses = None
        if 'labelClasses' in modelFile.attrs:
            labelClasses = literal_eval(modelFile.attrs.get('labelClasses'))
        return self.model, labelClasses

    def createModel(self, settings):
        print("Create Model")
        data_dir = pathlib.Path(settings.getDatasetPath())
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
        
        train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

        num_classes = len(self.class_names)

        model = keras.Sequential([
            keras.layers.Rescaling(1./255, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
            keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
            keras.layers.MaxPooling2D(),
            keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
            keras.layers.MaxPooling2D(),
            keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
            keras.layers.MaxPooling2D(),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(num_classes)
        ])
        
        model.compile(optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])

        return [model, train_ds, val_ds, self.class_names]

    def trainModel(self, train_ds, val_ds, class_names, settings, currentCheckpoint=0):
        print("train model")
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=settings.getCheckpointPath(), save_weights_only=True, verbose=1, save_freq='epoch')

        epochs = EPOCHS - currentCheckpoint
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=[cp_callback]
        )
        self.saveModel(settings, class_names)
    
    def trainModelWithDataAugmentation(self, train_ds, val_ds, class_names, settings, currentCheckpoint=0):
        data_augmentation = keras.Sequential([
            keras.layers.RandomFlip("horizontal", input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
            keras.layers.RandomRotation(0.1),
            keras.layers.RandomZoom(0.1),
        ])
        self.model = keras.Sequential([
            data_augmentation,
            keras.layers.Rescaling(1./255),
            keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
            keras.layers.MaxPooling2D(),
            keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
            keras.layers.MaxPooling2D(),
            keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
            keras.layers.MaxPooling2D(),
            keras.layers.Dropout(0.2),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(len(class_names), name="outputs")
        ])

        self.model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=settings.getCheckpointPath(), save_weights_only=True, verbose=1, save_freq='epoch')

        epochs = EPOCHS_DATA_AUG - currentCheckpoint
        history = self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=[cp_callback]
        )
        self.saveModel(settings, class_names)

    def saveModel(self, settings, class_names):
        labels_string = json.dumps(class_names)
        self.model.save_weights(settings.getCheckpointPath().format(epoch=0))
        self.model.save(settings.getCheckpointDir()+"/model.h5")
        if labels_string is not None:
            f = h5py.File(settings.getCheckpointDir()+"/model.h5", mode='a')
            f.attrs['labelClasses'] = labels_string
            f.close()

    def testModel(self, imageUrl):
        img = tf.keras.utils.load_img(
            imageUrl, target_size=(IMG_HEIGHT, IMG_WIDTH)
        )
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        
        predictions = self.model.predict(img_array, verbose=0)
        predictionsSoftMax = tf.nn.softmax(predictions[0])
        prediction_probabilities = tf.math.top_k(predictionsSoftMax, k=5)
        scores = prediction_probabilities.values.numpy()
        classEntries = prediction_probabilities.indices.numpy()
        predictionsResponse = []
        for prediction, indexModel in zip(scores, classEntries):
            accuracy = float(100) * float(prediction)
            model = self.labelClasses[indexModel]
            predictionsResponse.append({
                "accuracy": float("{:.3f}".format(accuracy)),
                "model": model
            })
        return predictionsResponse

model = Model("flowers")