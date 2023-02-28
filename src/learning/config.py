CONFIG = {
    "training": {
        "num_communication_rounds": 3,
        "num_samples": 10,
        "local_batch_size": 32,
        "local_epochs": 1,
        "num_trainers": 1,
        "trainer_name_prefix": "trainer",
    },
    "distribution": {
        "pyamqp_ip": "10.244.18.116",
        "aggregator_ip": "0.0.0.0",
        "trainer_ip": "0.0.0.0",
    },
}

TRAINER_MAP = {"name"}
