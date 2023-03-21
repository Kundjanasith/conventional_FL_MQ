import json

from celery.signals import celeryd_after_setup

import utils
from app import app
from learning.aggregator import Aggregator
from learning.config import CONFIG
from learning.trainer import Trainer


@celeryd_after_setup.connect
def capture_worker_name(sender, headers=None, body=None, **kwargs):
    sender_name = str(sender).split("@")[0]
    print(f"sender: {sender}, sender_name: {sender_name}")
    CONFIG["sender_name"] = sender_name


@app.task()
def celery_aggregate(list_local_models: dict, global_epoch: int) -> None:
    print(f"Starting epoc # {global_epoch}")
    trainers_bound = int(CONFIG["training"]["num_trainers"]) + 1
    # for idx in range(1, trainers_bound):
    #     name_prefix = CONFIG["training"]["trainer_name_prefix"]
    #     queue_name = f"{name_prefix}{idx}"
    #     aggr = Aggregator()
    #     aggregated_model = aggr.aggregate(list_local_models, global_epoch)
    #     if global_epoch < CONFIG["training"]["num_communication_rounds"]:
    #         print(f"sending epoc # {global_epoch} to {queue_name}")
    #         celery_train.apply_async(
    #             kwargs={
    #                 "model_weights": aggregated_model,
    #                 "global_epoch": global_epoch,
    #                 "queue_name": queue_name,
    #             },
    #             queue=queue_name,
    #         )
    
    for idx in range(1,trainers_bound):
        aggr = Aggregator()
        aggregated_model = aggr.aggregate(list_local_models, global_epoch)
        name_prefix = CONFIG["training"]["trainer_name_prefix"]
        queue_name = f"{name_prefix}{idx}"
        print(trainers_bound,queue_name)
        list_local_models[queue_name] = aggregated_model
        celery_train.apply_async(kwargs={"list_local_models": list_local_models,"global_epoch": global_epoch},queue=queue_name)
    # print(list_local_models.keys())
    # celery_train.apply_async(kwargs={"list_local_models": list_local_models,"global_epoch": global_epoch})
    # print('complete agg')

@app.task()
def celery_train(list_local_models: dict, global_epoch: int) -> None:
    print('strat trainer',list_local_models.keys())
    for queue_name in list_local_models.keys():
        trainer = Trainer()
        trained_model = trainer.train(queue_name, list_local_models[queue_name], global_epoch)
        model_weights = json.dumps(trained_model, cls=utils.NumpyArrayEncoder)
        list_local_models[queue_name] = model_weights
    celery_aggregate.apply_async(kwargs={"list_local_models": list_local_models,"global_epoch": global_epoch},queue="aggregator")


# @app.task()
# def celery_train(queue_name: str, model_weights, global_epoch) -> None:
#     print(f"Received epoc # {global_epoch}")
#     trainer = Trainer()
#     trained_model = trainer.train(queue_name, model_weights, global_epoch)
#     model_weights = json.dumps(trained_model, cls=utils.NumpyArrayEncoder)
#     list_model_weights = {}
#     # list_model_weights["sender_name"] = CONFIG["sender_name"]
#     # list_model_weights["queue_name"] = queue_name
#     # list_model_weights["weights"] = model_weights
#     list_model_weights[queue_name] = model_weights
#     celery_aggregate.apply_async(
#         kwargs={
#             "list_local_models": list_model_weights,
#             "global_epoch": global_epoch + 1,
#         },
#         queue="aggregator",
#     )
