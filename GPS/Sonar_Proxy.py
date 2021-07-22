from random import randrange

class Sonar(object):
    
    def __init__(self, callback):
        self.callback = callback
        
    def get(self):
        depth = randrange(10, 300)
        data = {'name': "SDDBT", 'data':{"depth": round(depth/10, 1)}}
        self.callback(data)
        temp = randrange(150, 280)
        data = {'name': "YXMTW", 'data': {"temp": round(temp/10, 1)}}
        self.callback(data)
        
def call(value):
    print(value)
        
def test():
    s = Sonar(call)
    for x in range(10):
        s.get()
        
if __name__ == "__main__":
    test()
        
        