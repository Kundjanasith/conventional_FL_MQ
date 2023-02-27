from learning.tasks import trainer, aggregator
import sys, configparser, json, utils
import numpy as np

def main():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    num_communication_rounds = int(config['TRAINING']['NUM_COMMUNICATION_ROUNDS'])
    list_model_weights = {} 
    for r in range(num_communication_rounds):
        print(r, len(list_model_weights))
        res = aggregator.apply_async(kwargs={'list_local_models': list_model_weights, 'global_epoch': r}, queue='aggregator', countdown=2)
        result = res.get(propagate=False)
        if res.state == 'SUCCESS':
            list_model_weights = {}
            res1 = trainer.apply_async(kwargs={'model_weights': result, 'global_epoch': r, 'queue_name': 'trainer1'}, queue='trainer1', countdown=2)
            res2 = trainer.apply_async(kwargs={'model_weights': result, 'global_epoch': r, 'queue_name': 'trainer2'}, queue='trainer2', countdown=2)
       
            result = res1.get(propagate=False)
            print(res1.state)
            if res1.state == 'SUCCESS':
                # list_model_weights.append(result)
                list_model_weights['trainer1'] = result
                # c = collector.apply_async(kwargs={'queue_name': 'trainer1', 'trained_model': res1, 'global_epoch': r}, queue='aggregator', countdown=2)
                # c.get(propagate=False)
            result = res2.get(propagate=False)
            print(res2.state)
            if res2.state == 'SUCCESS':
                # list_model_weights.append(result)
                list_model_weights['trainer2'] = result
                # c = collector.apply_async(kwargs={'queue_name': 'trainer2', 'trained_model': res2, 'global_epoch': r}, queue='aggregator', countdown=2)
                # c.get(propagate=False)
        

            # list_model_weights = np.array(list_model_weights)
            # list_model_weights = json.dumps(list_model_weights, cls=utils.NumpyArrayEncoder)
            # trained_models = utils.Models(list_model_weights)

            # print(type(list_model_weights),type(json.dumps(list_model_weights)))
            # print(type(res1),type(res2))
            # print('xx',len(list_model_weights))
        # break
        if r == 3:
            break
    


    # res = train.apply_async((), queue=q, countdown=2)
    # result = res.get(timeout=4, propagate=False)
    # print(result)
    # print(res.failed())
    # print(res.successful())
    # print(res.state)

if __name__ == '__main__':
    main()
