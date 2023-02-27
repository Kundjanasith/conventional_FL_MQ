from app import app
from learning.trainer import Trainer
from learning.aggregator import Aggregator

@app.task()
def trainer(queue_name, model_weights, global_epoch):
    t = Trainer()
    trained_model = t.training(queue_name, model_weights, global_epoch)

    # if data and data >= MAX_TRAINING_ROUNDS:
    #     print("training completed")
    #     return 0

    # t1 = Trainer()
    # result = t1.training_round(data)
    # print(f"Training data {result}")
    # aggregator.delay(trained_model, global_epoch+1)
    return trained_model

@app.task()
def aggregator(list_local_models, global_epoch):
    print('xxx-->'+str(global_epoch))
    a = Aggregator()
    aggregated_model = a.aggregate(list_local_models, global_epoch)
    # res1 = trainer.apply_async(kwargs={'model_weights': aggregated_model, 'global_epoch': r, 'queue_name': 'trainer1'}, queue='trainer1', countdown=2)
    # res2 = trainer.apply_async(kwargs={'model_weights': aggregated_model, 'global_epoch': r, 'queue_name': 'trainer2'}, queue='trainer2', countdown=2)
    # # trained_model1 = trainer.delay('trainer1', aggregated_model, global_epoch)
    # # trained_model2 = trainer.delay('trainer2', aggregated_model, global_epoch)
    # result1 = res1.get(propagate=False)
    # result2 = res2.get(propagate=False)
    # list_local_models = [result1,result2]
    # aggregated_model = a.aggregate(list_local_models, global_epoch)
    return aggregated_model

@app.task()
def test(global_epoch):
    print('--->',global_epoch)
    return global_epoch

# @app.task()
# def aggregator(global_epoch):
#     a = Aggregator()
#     aggregated_model = a.aggregate(global_epoch)
#     trainer.delay(aggregated_model, global_epoch)
#     return aggregated_model

# @app.task()
# def collector(queue_name, trained_model, global_epoch):
#     a = Aggregator()
#     res = a.collect(queue_name, trained_model, global_epoch)
#     return res.id