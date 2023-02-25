from fedlearn.tasks import train
from fedlearn.utils import MAX_TRAINING_ROUNDS
import sys, configparser

def main():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    num_communication_rounds = int(config['TRAINING']['NUM_COMMUNICATION_ROUNDS'])
    for r in range(num_communication_rounds):
        
    


    res = train.apply_async((), queue=q, countdown=2)
    result = res.get(timeout=4, propagate=False)
    print(result)
    print(res.failed())
    print(res.successful())
    print(res.state)

if __name__ == '__main__':
    main()
