#!/bin/bash

mode=trainer
[ -z $1 ] || mode=$1
echo "Operational mode is $mode"

cd /conventional_FL_MQ
source venv/bin/activate

if [ "$mode" == "trainer" ]; then
    mkdir trainer_storage/aggregator_models trainer_storage/trainer_models
    celery -A learning.tasks worker --without-heartbeat --without-gossip --without-mingle --loglevel=INFO -Q trainer1 --concurrency=1 -n trainer1@%h
elif [ "$mode" == "aggregator" ]; then
    mkdir aggregator_storage/aggregator_models aggregator_storage/trainer_models
    python3 start_training.py
else
    echo "Invalid mode $mode"
fi

