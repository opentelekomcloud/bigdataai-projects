# Labenv examples

![image info](./screenshots_formd/ai_libs.jpg)



### Introduction
Labenv examples are created for the users of the conda environments so they are able to test the packages and get an insight how setup and training models can be done quickly and easily.

### Summary 
You can find all the example scripts via the path written below:
```
cd ~/ai-image/ansible/files/ai-examples
```

### Preparation to run a custom example script


After you navigate into the ai_examples folder you can test the conda environment by choosing a training script from below:
```                 
mnist_pytorch.py  
pytorch_training_example.py
start_tf_mnist_training.sh
tf_serving_prerequisite.sh
mnist_client.py
mnist_saved_model.py
start_keras_mnist_training.sh
start_tf_model_server.sh
mnist_input_data.py    
mxnet16_training_example.py
start_mxnet_mnist_training.sh
test_tf_serving.sh
mnist_keras_convnet.py
mxnet19_training_example.py
start_pytorch_mnist_training.sh
tf115training_example.py
mnist_mxnet.py
pytorch110_training_example.py 
start_tf_mnist_test_client.sh 
tf2_training_example.py
```


Run any script by entering the keyword python in front of the name of the script:
```
python tf2_training_example.py
```
Once the script is started it will produce an output like this:
```
(tf27) ubuntu@ecs4-tf:/tmp/ai-image/ansible/files/ai-examples$ python tf2_training_example.py
TensorFlow version: 2.7.1
2022-03-30 14:45:52.961432: I tensorflow/core/platform/cpu_feature_guard.cc:151] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 AVX512F FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
2022-03-30 14:45:53.544150: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1525] Created device /job:localhost/replica:0/task:0/device:GPU:0 with 14636 MB memory:  -> device: 0, name: Tesla V100-SXM2-16GB, pci bus id: 0000:21:01.0, compute capability: 7.0
Epoch 1/5
1875/1875 [==============================] - 3s 1ms/step - loss: 0.2946 - accuracy: 0.9131
Epoch 2/5
1875/1875 [==============================] - 3s 1ms/step - loss: 0.1413 - accuracy: 0.9579
Epoch 3/5
1875/1875 [==============================] - 3s 1ms/step - loss: 0.1072 - accuracy: 0.9675
Epoch 4/5
1875/1875 [==============================] - 3s 1ms/step - loss: 0.0893 - accuracy: 0.9726
Epoch 5/5
1875/1875 [==============================] - 3s 1ms/step - loss: 0.0756 - accuracy: 0.9763
