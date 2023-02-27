from app import app
from learning.trainer import Trainer
from learning.aggregator import Aggregator

@app.task()
def trainer(model_weights):
    t = Trainer()
    result = t.training(model_weights)

    # if data and data >= MAX_TRAINING_ROUNDS:
    #     print("training completed")
    #     return 0

    # t1 = Trainer()
    # result = t1.training_round(data)
    # print(f"Training data {result}")
    result = aggregate.delay(result)
    return result.id

@app.task()
def aggregator(global_epoch):
    a = Aggregator()
    aggregated_model = a.aggregate(global_epoch)
    trainer.delay(aggregated_model)
    return aggregated_model
