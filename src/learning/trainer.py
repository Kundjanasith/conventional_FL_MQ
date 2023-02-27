from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.backend import clear_session
import utils, configparser
import h5py, json
import numpy as np 
import base64
import json
from json import JSONEncoder

def load_dataset():
    (X_train, Y_train), (X_test, Y_test) = cifar10.load_data()
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train = X_train / 255.0
    X_test = X_test / 255.0
    Y_train = to_categorical(Y_train)
    Y_test = to_categorical(Y_test)
    return (X_train, Y_train), (X_test, Y_test)

def sampling_data(num_samples):
    (x_train, y_train), (x_test, y_test) = load_dataset()
    print(len(x_train))
    num_of_each_dataset = num_samples
    print(num_of_each_dataset)
    split_data_index = []
    while len(split_data_index) < num_of_each_dataset:
        item = random.choice(range(x_train.shape[0]))
        if item not in split_data_index:
            split_data_index.append(item)
    new_x_train = np.asarray([x_train[k] for k in split_data_index])
    new_y_train = np.asarray([y_train[k] for k in split_data_index])
    return new_x_train, 

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class Trainer():

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        self.num_samples = int(config['TRAINING']['NUM_SAMPLES'])
        self.local_batch_size = int(config['TRAINING']['LOCAL_BATCH_SIZE'])
        self.local_epochs = int(config['TRAINING']['LOCAL_EPOCHS'])

    def training(self, model_weights):
        # print(model)
        # print('x',model_weights)
        print('1')
        model = utils.model_init()
        print('2')
        model_weights = json.loads(model_weights)
        print(type(model_weights))
        # model_weights = np.array(model_weights)
        # print('3x',type(model_weights))
        # x = base64.b64decode(model_weights)
        # print('3.5',type(x))
        # model_weights = np.load(model_weights)
        # print('4',type(model_weights))
        # model.set_weights(model_weights)
        # model.save_weights('trainer_storage/aggregator_models/model_ep%d.h5'%(global_epoch))
        # print('5')
        # model.load_weights('trainer_storage/aggregator_models/model_ep%d.h5'%(global_epoch))
        # x_train, y_train = sampling_data(self.num_samples)
        # model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
        # model.fit(x_train, y_train,epochs=self.local_epochs,batch_size=self.local_batch_size,verbose=1,validation_split=0.2)
        # model.save_weights('trainer_storage/trainer_models/%s_ep%d.h5'%(hostname,global_epoch+1))
        return model 
        
