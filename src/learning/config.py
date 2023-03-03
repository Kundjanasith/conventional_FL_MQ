CONFIG = {
    "training": {
        "num_communication_rounds": 1000,
        "num_samples": 100,
        "local_batch_size": 8,
        "local_epochs": 5,
        "num_trainers": 5,
        "trainer_name_prefix": "trainer",
    },
    "distribution": {
        "pyamqp_ip": "10.10.100.1",
        "aggregator_ip": "0.0.0.0",
        "trainer_ip": ["0.0.0.0", "0.0.0.0"],
    },
}

TRAINER_MAP = {"name"}
