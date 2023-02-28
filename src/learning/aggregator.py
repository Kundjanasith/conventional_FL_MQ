import json

import numpy as np
from tensorflow.keras.backend import clear_session

import utils


def getLayerIndexByName(model, layername):
    for idx, layer in enumerate(model.layers):
        if layer.name == layername:
            return idx


def aggregation(model_path):
    global_model = utils.model_init()
    global_model.load_weights(model_path[0])
    model_dict = {}
    count = 0
    for global_layer in global_model.layers:
        l_idx = getLayerIndexByName(global_model, global_layer.name)
        for w_idx in range(len(global_model.get_layer(index=l_idx).get_weights())):
            w = global_model.get_layer(index=l_idx).get_weights()[w_idx]
            model_dict[count] = []
            model_dict[count].append(w)
            count = count + 1
    clear_session()
    for mod_path in model_path[1:]:
        count = 0
        client_model = utils.model_init()
        print(mod_path)
        client_model.load_weights(mod_path)
        for client_layer in client_model.layers:
            l_idx = getLayerIndexByName(client_model, client_layer.name)
            for w_idx in range(len(client_model.get_layer(index=l_idx).get_weights())):
                w = client_model.get_layer(index=l_idx).get_weights()[w_idx]
                model_dict[count].append(w)
                count = count + 1
    clear_session()
    aggregated_model = utils.model_init()
    count = 0
    for aggr_layer in aggregated_model.layers:
        l_idx = getLayerIndexByName(aggregated_model, aggr_layer.name)
        w_arr = []
        for w_idx in range(len(aggregated_model.get_layer(index=l_idx).get_weights())):
            w = aggregated_model.get_layer(index=l_idx).get_weights()[w_idx]
            w_avg = np.nanmean(np.array(model_dict[count]), axis=0)
            count = count + 1
            w_arr.append(w_avg)
        aggregated_model.get_layer(index=l_idx).set_weights(w_arr)
    return aggregated_model


class Aggregator:
    def aggregate(self, list_local_models: dict, global_epoch: int):
        model = utils.model_init()
        if global_epoch == 0:
            print("Loading initial model paramters . . .")
            model.save_weights("aggregator_storage/aggregator_models/model_ep0.h5")
        else:
            model.save_weights(
                f"aggregator_storage/aggregator_models/model_ep{global_epoch}.h5"
            )

        model.load_weights("aggregator_storage/aggregator_models/model_ep0.h5")
        model_weights = model.get_weights()
        model_weights = json.dumps(model_weights, cls=utils.NumpyArrayEncoder)
        return model_weights
