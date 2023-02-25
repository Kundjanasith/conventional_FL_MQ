import utils 

class Aggregator():
    
    def __init__(self, hostname='aggregator', global_epoch):
        self.global_epoch = global_epoch
        self.global_model = utils.model_init()

    def aggregate(self):
        if self.global_epoch == 0:
            print('Initial model . . .')
        else:
            print('Load global model %d'%(self.global_epoch))
            model.load_weights

