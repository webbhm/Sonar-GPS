from GPS import GPS

class Location(object):

    def __init__(self):
        #print("Init")
        '''get callback and setup GPS'''
        self._callback = self.handler
        self._gps = GPS(self._callback)
        #self._gps.watch()
        self._value = None
        #print("Finish Init")

    def handler(self, value):
        #print("Handler", value)
        self._value = value
    
    def getLoc(self):
        #print("In getLoc")
        while self._value == None:
            self._gps.getSentence()
        return self._value
        
    
def test():
    print("Test Location")
    loc = Location()
    l = loc.getLoc()
    print(l)

if __name__=="__main__":
    test()    