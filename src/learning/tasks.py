from app import app
from learning.trainer import Trainer
from learning.aggregator import Aggregator

@app.task
def train(data=None):
    t = Trainer()
    
    # if data and data >= MAX_TRAINING_ROUNDS:
    #     print("training completed")
    #     return 0

    # t1 = Trainer()
    # result = t1.training_round(data)
    # print(f"Training data {result}")
    # result = rollup.delay(result)
    # return result.id

@app.task
def rollup(data):
    # agr = Aggregator()
    # new_data = agr.rollup_round(data)
    # print(f"Rollup data {new_data}")
    # train.delay(new_data)
