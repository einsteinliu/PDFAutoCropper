import datetime

class SteinTimer(object):
    """description of class"""
    def __init__(self):
        self.begin = datetime.datetime.now()
        self.end   = datetime.datetime.now()    
    def start(self):
        self.begin = datetime.datetime.now()
    
    def stop(self):
        self.end = datetime.datetime.now()
    
    def elapsed(self):
        return 1000*(self.end-self.begin).total_seconds()

