"""
Revised Monitor for screen addition, removing logging & LED
Author: Howard Webb
Date: 10/09/2018

Controller to collect GPS and Sonar data and integrate into a single record
May also collect non-serial data (ie. turbidity)
Store to a file, incrementing for each new run
"""
from __future__ import print_function
from GPS import GPS
from Sonar import Sonar
# from oneWireTemp import getTempC
# from Turbidity import Turbidity
import serial
# Routine to check serial ports for GPS or Sonar messages
# No guarantee which device is on which port
from PortScan import PortScan
from i2c_lcd_util import lcd
from time import sleep
from datetime import datetime

class Monitor(object):
    
    def __init__(self):
        """
        Build monitor with GPS and Sonar
        :param logger:
        """
        # Object level holders for data
        
        # used for recording
        self._time = None
        self._lat = None
        self._lon = None
        self._depth = None
        self._temp = None
        # used for dispaly
        self._time_msg = ""
        self._lat_msg = ""
        self._lon_msg = ""
        self._depth_msg = ""
        self._temp_msg = ""
        
        
        self._lcd = lcd()
        self._lcd.lcd_display_string("Waiting GPS", 1)
        # Option to use test logger or recording logger
        #        self._tur = Turbidity()
        # Get file for logging data
        self._file = self.getFile()
        self.writeHeader()
        self._GPS = None
        self._Sonar = None
        # Get list of ports and check who is using
        #  avoids problems when switch USB location
        ps = PortScan()
        port_list = ps.getPorts()
        print(port_list)
        if 'GPS' in port_list.keys():
            
            self._GPS = GPS(self.recorder, port_list['GPS'])
        else:
            # Fail gracefully
            self._GPS = None
            self._lcd.lcd_display_string("No GPS port found", 1)            
            raise SystemExit

        self._lcd.lcd_display_string("Waiting Sonar", 1)            
        if 'Sonar' in port_list.keys():
            self._Sonar = Sonar(self.recorder, port_list['Sonar'])
        else:
            # Fail 
            self._Sonar = None
            self._lcd.lcd_display_string("No Sonar found", 1)                        
            raise SystemExit
        self._lcd.lcd_display_string(" "*15)
        self._lcd.lcd_display_string("Data", 1, 1)        
        while True:
            self._GPS.get()
            self._Sonar.get()
            #sleep(0.5)
            
    def getFile(self):
        name = self.getFileName()
        return self.openFile(name)
    
    def getFileName(self):
        """
        Create file name for next log
            Assumes format 'Log_000.csv'
            Will incriment the number for the next file
        :return: the filename
        """
        import glob
        filename = '/home/pi/Data/Log_000.csv'
        files = glob.glob("/home/pi/Data/*.csv")
        if len(files) > 0:
            files.sort()
            last_file = files[-1]
            next_nbr = int(last_file.split('.')[0].split('_')[1])
            next_nbr += 1
            filename = "{}{}{}".format('/home/pi/Data/Log_', format(next_nbr, '0>3'), '.csv')
        return filename

    def openFile(self, name):
        """
        Open a file for logging data
        :return: the file descriptor
        """
        return open(name, 'a')
    
    def writeHeader(self):
        # write header
        rec = "{}, {}, {}, {}, {}".format('Time', 'Latitude', 'Longitude', 'Depth', 'Temperature')
        self.save(rec)

    def save(self, rec):
        """
        appandes the characters in rec into the file
        :param rec: the characters to be saved
        :return: None, but also prints the rec
        """
        self._file.write(rec)
        self._file.flush()

    def recorder(self, values):
        """
        Callback to get messages, when have all three - save them as one record. A log value is printed
        when all measurement values have non None values.
        :param values:
        :return: None
        """
        #        print "Values", values
        # gets data from GPS and Sonar
        #print(values)
        #print(values["name"])
        if values['name'] is None:
            print("No Msg Name")
        if values['name'] == 'GPRMC':  # Time and velocity
            #print("GPRMC", values)
            self._time = values["data"]["time"]
            self._lat = values["data"]["lat"]
            self._lon = values["data"]["lon"]
        
            self._lat_msg = '{:.6f}'.format(self._lat)
            self._lon_msg = '{:.6f}'.format(self._lon)        
            
        if values['name'] == 'GPGLL':  # Time and location
            print("GPGLL", values)
            self._time = values["data"]["time"]
            self._lat = values["data"]["lat"]
            self._lon = values["data"]["lon"]
        
            self._lat_msg = '{:.6f}'.format(self._lat)
            self._lon_msg = '{:.6f}'.format(self._lon)        
            
        elif values['name'] == 'SDDBT':  # Depth
            #print("SDDBT", values)
            depth = values["data"]["depth"]
            # check for missing data
            if depth == '':
                depth = 0
            self._depth = depth    
            #print(type(self._depth), self._depth)
            self._depth_msg = 'D{:04.1f}'.format(float(self._depth))
            
        elif values['name'] == 'YXMTW':  # Temperature
            #print("YXMTW", values)
            self._temp = values["data"]["temp"]
            #print(type(self._temp), self._temp)            
            self._temp_msg = 'T{}'.format(self._temp)
            
       # Save record when have all parts
        #print(datetime.now().strftime("%S"))
        #print(values["name"], self._lat, self._depth, self._time)
        if (self._lat is not None) and (self._depth is not None):
            print(values["name"], self._lat, self._depth, self._time)            
            self.finishLogging()

            # display data
            self._lcd.lcd_display_string(self._lat_msg, 1, 1)
            self._lcd.lcd_display_string(self._depth_msg, 1, 11)
            
            self._lcd.lcd_display_string(self._lon_msg, 2)        
            self._lcd.lcd_display_string(self._temp_msg, 2, 11)

            # clear data for next round of sentences
            self._time = None
            self._lat = None
            self._lon = None
            self._depth = None
            self._temp = None

    def finishLogging(self):
        """
        save the logging data to the file
        :return: None
        """
        rec = "\n{}, {}, {}, {}, {}".format(self._time, self._lat, self._lon, self._depth, self._temp)
        self.save(rec)


def test():
    """ Quick test with dummy logger """
    print("Test Monitor")
    main()

def main():    
    mon = Monitor()

if __name__ == "__main__":
        main()
