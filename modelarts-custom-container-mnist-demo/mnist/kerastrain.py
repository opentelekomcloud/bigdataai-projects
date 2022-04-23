from __future__ import print_function
import os
import sys
# for getting the dataset
import gzip
import pickle
# for the model building
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import json
import argparse
# for copying the model to OBS
from otc_obs_util import *

# training parameters
batch_size = 32
num_classes = 10
epochs = 1

# input image dimensions
img_rows, img_cols = 28, 28
FLAGS=None

def main():
    # get the compressed dataset
    with gzip.open(FLAGS.data_dir +'/mnist.pkl.gz', 'rb') as f:
        (x_train, y_train), (x_test, y_test) = pickle.load(f, encoding='latin-1')
    # format the train and test arrays
    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    # build the sequential model with the layers
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])
    # start training the model
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(x_test, y_test))
    # see the results of the model
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    with open('model.json', 'w') as outfile:
        json.dump(model.to_json(), outfile)
    # create a folder for the output files locally
    if not os.path.exists('mnist_data_out'):
      os.makedirs('mnist_data_out')
    # save the weights of the model into the local folder
    model.save_weights('mnist_data_out/weights2.h5')
    # copy the output folder with the files into OBS
    upload_files_to_s3(Bucket="customcontainer",
                               input_dir="mnist_data_out", # this is directory
                               output_dir="mnist_data_out/"
                               )


if __name__ == '__main__':
  # set the arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', '--data_url', type=str, default='mnist_data',
                      help='Directory for storing input data')
  parser.add_argument('--train_dir', '--train_url', type=str, default='./',
                      help='Directory for storing trained data output ')
  FLAGS, unparsed = parser.parse_known_args()
  main()

