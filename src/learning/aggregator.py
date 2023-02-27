import utils, glob
from tensorflow.keras.backend import clear_session
import h5py
import pickle, json
import json
from json import JSONEncoder
import base64
import numpy as np

def getLayerIndexByName(model, layername):
    for idx, layer in enumerate(model.layers):
        if layer.name == layername:
            return idx

def aggregation(model_path):
    global_model = model_init()
    global_model.load_weights(model_path[0])
    model_dict = {}
    count = 0
    for l in global_model.layers:
        l_idx = getLayerIndexByName(global_model, l.name)
        for w_idx in range(len(global_model.get_layer(index=l_idx).get_weights())):
            w = global_model.get_layer(index=l_idx).get_weights()[w_idx]
            model_dict[count] = []
            model_dict[count].append(w)
            count = count + 1
    clear_session()
    for p in model_path[1:]:
        count = 0
        client_model = model_init()
        print(p)
        client_model.load_weights(p)
        for l in client_model.layers:
            l_idx = getLayerIndexByName(client_model, l.name)
            for w_idx in range(len(client_model.get_layer(index=l_idx).get_weights())):
                w = client_model.get_layer(index=l_idx).get_weights()[w_idx]
                model_dict[count].append(w)
                count = count + 1
    clear_session()
    aggregated_model = model_init()
    count = 0
    for l in aggregated_model.layers:
        l_idx = getLayerIndexByName(aggregated_model, l.name)
        w_arr = []
        for w_idx in range(len(aggregated_model.get_layer(index=l_idx).get_weights())):
            w = aggregated_model.get_layer(index=l_idx).get_weights()[w_idx]
            w_avg = np.nanmean(np.array(model_dict[count]),axis=0)
            count = count + 1
            w_arr.append(w_avg)
        aggregated_model.get_layer(index=l_idx).set_weights(w_arr)
    return aggregated_model



class Aggregator():
    
    # def __init__(self):
    #     self.global_epoch = global_epoch

    def aggregate(self, list_local_models, global_epoch):
        model = utils.model_init()
        print('---->'+str(len(list_local_models))+str(global_epoch))
        if global_epoch == 0:
            print('Initial model . . .')
            model.save_weights('aggregator_storage/aggregator_models/model_ep0.h5')
            model.load_weights('aggregator_storage/aggregator_models/model_ep0.h5')
            model_weights = model.get_weights()
            model_weights = json.dumps(model_weights, cls=utils.NumpyArrayEncoder)
            return model_weights
        else:
            print('xxxxx')
            print(len(list_local_models))
            for i in list_local_models:
                print(i)
            
            print(glob.glob('aggregator_storage/trainer_models/*_ep%d.h5'%global_epoch))
            model.save_weights('aggregator_storage/aggregator_models/model_ep%d.h5'%global_epoch)
            model.load_weights('aggregator_storage/aggregator_models/model_ep0.h5')
            model_weights = model.get_weights()
            model_weights = json.dumps(model_weights, cls=utils.NumpyArrayEncoder)
            return model_weights

            # print('tem list of model weights',len(list_model_weights))
            # for i in list_model_weights.keys():
            #     print(i)
            #     print(type(list_model_weights[i]))
            # print('Load global model %d'%(global_epoch))
            # model_paths = ['aggregator_storage/aggregator_models/model_ep%d.h5'%(self.global_epoch-1)]
            # for p in glob.glob('aggregator_storage/trainer_models/*_ep%d.h5'%(self.global_epoch-1)):
            #     model_paths.append(p)
            # aggregated_model = aggregation(model_paths)
            # aggregated_model.save_weights('aggregator_storage/aggregator_models/model_ep%d.h5'%(self.global_epoch))
            # aggregated_model.load_weights('aggregator_storage/aggregator_models/model_ep%d.h5'%(self.global_epoch))
            # res = h5py.File('aggregator_storage/aggregator_models/model_ep%d.h5'%(self.global_epoch), 'r')
            return 'p'

    # def collect(self, queue_name, model_weights, global_epoch):
    #     model = utils.model_init()
    #     model_weights = json.loads(model_weights)
    #     model_weights = np.asarray(model_weights, dtype=object)
    #     model = utils.load_weights(model, model_weights)
    #     model.save_weights('aggregator_storage/trainer_models/%s_ep%d.h5'%(queue_name,global_epoch))
    #     return 'store aggregator_storage/trainer_models/%s_ep%d.h5'%(queue_name,global_epoch)
