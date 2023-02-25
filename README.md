# conventional_FL_MQ

```
docker pull rabbitmq:management
```
```
docker run --rm -d -p 15671:15671/tcp -p 15672:15672/tcp -p 15691:15691/tcp -p 15692:15692/tcp -p 25672:25672/tcp -p 4369:4369/tcp -p 5671:5671/tcp -p 5672:5672/tcp rabbitmq: management
```

```
celery -A fedlearn.tasks worker --loglevel=INFO -Q aggr1 --concurrency=1 -n aggr1@%h
celery -A fedlearn.tasks worker --loglevel=INFO -Q trainer1 --concurrency=1 -n trainer1@%h
python3 start_training.py
```