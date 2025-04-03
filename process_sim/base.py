# process_sim/base.py

class ProcessComponent:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def update(self):
        raise NotImplementedError("Must implement update method.")
    
    def publish(self):
        raise NotImplementedError("Must implement publish method.")
