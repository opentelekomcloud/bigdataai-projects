#!/usr/bin/env python
from flask import Flask, jsonify, render_template, request
# for model operations
import tensorflow as tf
from keras.models import load_model
from tensorflow.keras.models import load_model
from tensorflow.python.keras.backend import set_session
import keras.models
from scipy.misc import imread, imresize,imshow
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import numpy as np
# for preprocessing the image
from skimage.transform import resize as imresize
from scipy.misc import imread, imresize,imshow
from PIL import Image
import imageio
# standard python libraries
import warnings
import re
import os
import base64
import json
import logging
# for copying files from OBS to the container
from otc_obs_util import *

app = Flask(__name__)
# for defining the global variables
model = None
graph = None
sess = None


# print environment variables and files for debugging purposes
def mnlogger():
    print(os.environ)
    for root, dirs, files in os.walk("/home/work"):
      path = root.split(os.sep)
      print((len(path) - 1) * '---', os.path.basename(root))
      for file in files:
        print(len(path) * '---', file)

# transfer files from OBS into the container so they can be used locally for inference
def get_model_from_obs():
    download_files_from_s3(Bucket="customcontainer",
                           input_dir="mnist_data_out",
                           output_dir="."
                          )
# this function initalizes the model from the trained model
def init():
    global graph
    global sess
    graph = tf.get_default_graph()
    sess = tf.Session()
    set_session(sess)
    # for debug purposes
    mnlogger()
    # trained model is being transferred
    get_model_from_obs()
    num_classes = 10
    img_rows, img_cols = 28, 28
    input_shape = (img_rows, img_cols, 1)
    # building the model with the appropriate layers
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))
    model.load_weights("/home/work/mnist_data_out/weights2.h5")
    model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])
    return model

# this endpoint is needed for prediction not the /predict!
@app.route('/', methods=['GET','POST'])
def predict():
    # get data from drawing canvas and save as image
    filelist = request.files.getlist("images")
    print( filelist )
    image1 = Image.open(filelist[0])
    image1 = np.array(image1, dtype=np.float32)
    image1.resize((1, 28, 28))

    # reshape image data for use in neural network
    x = image1.reshape(1,28,28,1)
    # we initialize the model
    global model
    if not model:
        model = init()
    # this is how we get the inference's output
    with graph.as_default():
        out = model.predict(x)
    print(out)
    print(np.argmax(out, axis=1))
    arr_argsorted=np.argsort(out[0])

    # dict_output should look like this {"predicted_label":"3", "scores":[["3","0.83"], ["8","0.1"]]}
    dict_output = {"predicted_label":str(np.argmax(out, axis=1)[0]), "scores":[[str(arr_argsorted[-1]), str(round(out[0][arr_argsorted[-1]]*100, 2))],
                                                                               [str(arr_argsorted[-2]), str(round(out[0][arr_argsorted[-2]]*100, 2))],
                                                                               [str(arr_argsorted[-3]), str(round(out[0][arr_argsorted[-3]]*100, 2))]]}
    return jsonify(dict_output)



@app.route('/predict', methods=['GET','POST'])
def root():
    return jsonify({'result': '1'})

@app.route('/health')
def health():
    return jsonify({'health': 'true'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=False, port=8080)

