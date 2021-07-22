"""
USB GPS handler, simple serial reader with parsing
Note: Only one consumer can use this object because serial ports cannot be shared
Sentence: RMC
0 - sentence
1 - UTC of fix
2 - Status A=active, V=void
3 - Latitude
4 - Longitude
5 - Speed (knots)
6 - Track angle in degrees
7 - Date
8 - Magnetic variance
9 - checksum

Author: Howard Webb
Date: 2018/10/04

"""
from __future__ import print_function
import serial
from PortScan import PortScan
import datetime


class GPS(object):
    ''' GPS object '''

#    def __init__(self, callback, port='/dev/ttyUSB0'):
    def __init__(self, callback, port=None):
        """
        Get the GPS data and print it with the callback function
        :param callback: The callback function
        :param port: The port for the GPS
        """
        self._callback = callback
            
        if port == None:
            port = self.findPort()
        self._port = None
        try:
            self._port = serial.Serial(port, baudrate=4800, timeout=1)
        except Exception as e:
            print(e)
            
    def findPort(self):
        ps = PortScan()
        port_list = ps.getPorts()
        if 'GPS' in port_list.keys():
            return port_list['GPS']
        else:
            return None

    def watch(self):
        """
        infinite loop to watch the GPS. For each new record, parse it and pass it to the callback
        :return:
        """
        while True:
            self.get()

    # noinspection PyUnusedLocal
    def get(self):
        """
        reads the gPS value and prints it with the callback function
        :return: None
        """

        if self._port is None:
            values = {'name': None, 'data': None}
            self._callback(values)
            return

        if self._port.inWaiting() > 0:
            ''' Get sentence without blocking '''
            new_data = self._port.readline().decode('ascii', errors='replace')
            #print("*", end='')
            if new_data:
                values = []
                sentence = new_data.split(',')
                #print("{} {}".format("Sentence", sentence[0]))
                values = None
                if sentence[0] == '$GPRMC':
                    #print("{} {}".format("Sentence", sentence[0]))
                    for word in sentence:
                        pass
                        #print("{}: {}".format("WORD", word))
                    date = '20' + sentence[9][4:6] + '-' + sentence[9][2:4] + '-' + sentence[9][0:2]
                    time = sentence[1][0:2] + ':' + sentence[1][2:4] + ':' + sentence[1][4:6]
                    timestamp = date + ' ' + time
                    #print(sentence)
                    #print(sentence[4])
                    LatDec = 0.0
                    if len(sentence[4]):
                        DD = int(float(sentence[3]) / 100)
                        SS = float(sentence[3]) - DD * 100
                        LatDec = round(DD + SS / 60, 6)
                        if sentence[4] == 'S':
                            LatDec = LatDec * -1

                    LonDec = 0.0
                    if len(sentence[5]):
                        DD = int(float(sentence[5]) / 100)
                        SS = float(sentence[5]) - DD * 100
                        LonDec = round(DD + SS / 60, 6)
                        if sentence[6] == 'W':
                            LonDec = LonDec * -1
    
                    #                        print "Time: ", timestamp, LatDec, LonDec
                    values = {'name': sentence[0][1:], 'data': {'time': timestamp, 'lat': LatDec, 'lon': LonDec}}
                    #                        print values
                '''                    
                if sentence[0] == '$GPGLL':
                    # best for UBlock GPS, does not tend to process GPRCL
                    #print(new_data)
                    for word in sentence:
                        pass
                        #print("{}: {}".format("WORD", word))
                    dt = str(datetime.date.today())
                    time = sentence[5][0:2] + ':' + sentence[5][2:4] + ':' + sentence[5][4:6]
                    timestamp = dt + ' ' + time
                    #print(sentence)
                    #print(sentence[4])
                    LatDec = 0.0
                    #print(sentence[1])
                    if len(sentence[1]):
                        DD = int(float(sentence[1]) / 100)
                        SS = float(sentence[1]) - DD * 100
                        LatDec = round(DD + SS / 60, 6)
                        if sentence[1] == 'S':
                            LatDec = LatDec * -1

                    LonDec = 0.0
                    print(sentence[3])
                    if len(sentence[3]):
                        DD = int(float(sentence[3]) / 100)
                        SS = float(sentence[3]) - DD * 100
                        LonDec = round(DD + SS / 60, 6)
                        if sentence[4] == 'W':
                            LonDec = LonDec * -1
    
                    #                        print "Time: ", timestamp, LatDec, LonDec
                    values = {'name': sentence[0][1:], 'data': {'time': timestamp, 'lat': LatDec, 'lon': LonDec}}
                    #                        print values
                    '''
                if values:
                    self._callback(values)


def testCallback(value):
    ''' callback for test, simply print content '''
    print(value)


def test():
    ''' Test function for GPS object '''
    print("Testing GPS")
    main()
    
def main():    
    ''' Test function for GPS object '''
    print("Testing GPS")
    s = GPS(testCallback)
    s.watch()


if __name__ == "__main__":
    main()
