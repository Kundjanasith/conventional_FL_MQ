from celery import Celery
import configparser, ast

config = configparser.ConfigParser()
config.read('../config.ini')

PYAMQP_IP = config['DISTRIBUTION']['PYAMQP_IP']
AGGRGATOR_IP = config['DISTRIBUTION']['AGGREGATOR_IP']
TRAINER_IP = config['DISTRIBUTION']['TRAINER_IP']

def task_routes_init():
    result = {}
    result['learning.tasks.aggregator'] = {'queue': 'aggregator'}
    for i in range(len(ast.literal_eval(config['DISTRIBUTION']['TRAINER_IP']))):
        result['learning.tasks.trainer'] = {'queue': 'trainer%d'%(i+1)}
     
app = Celery(
    "fedlearn",
    backend="rpc://",
    broker="pyamqp://myuser:mypassword@%s:5672/myvhost"%PYAMQP_IP,
    include=["learning.tasks"],
)

app.conf.update(
    result_expires=3600,
)

app.conf.update(
    task_routes = task_routes_init(),
)

if __name__ == "__main__":
    app.start()