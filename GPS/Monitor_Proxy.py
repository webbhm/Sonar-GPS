from GPS import GPS
from i2c_lcd_util import lcd
from Sonar_Proxy import Sonar
from time import sleep

class Monitor(object):
    
    def __init__(self):

        self._lat_msg = ""
        self._lon_msg = ""
        self._depth_msg = ""
        self._temp_msg = ""
        self._lat = None
        self._lon = None
        self._depth = None
        self._temp = None
        
        self._lcd = lcd()
        self._lcd.lcd_display_string("Waiting GPS", 1)
        self._gps = GPS(self.callback)
        self._lcd.lcd_display_string(" "*15)
        self._lcd.lcd_display_string("Waiting Sonar", 1)
        self._sonar = Sonar(self.callback)
        sleep(2)
        self._lcd.lcd_display_string(" "*15)
        self._lcd.lcd_display_string("Data", 1, 1)
        
        while True:
            self._gps.get()
            self._sonar.get()
            sleep(.5)
        
        
    def callback(self, values):
        # gets data from GPS and Sonar
        #print(value)
        print(values["name"])
        if values['name'] is None:
            print("No Msg Name")
        if values['name'] == 'GPRMC':  # Time and velocity
            print("GPRMC", values)            
            self._lat = values["data"]["lat"]
            self._lon = values["data"]["lon"]
        
            self._lat_msg = '{:.6f}'.format(self._lat)
            self._lon_msg = '{:.6f}'.format(self._lon)        
            
        if values['name'] == 'GPGLL':  # Time and location
            print("GPGLL", values)
            
            self._lat = values["data"]["lat"]
            self._lon = values["data"]["lon"]
        
            self._lat_msg = '{:.6f}'.format(self._lat)
            self._lon_msg = '{:.6f}'.format(self._lon)        
            
        elif values['name'] == 'SDDBT':  # Depth
            #print("SDDBT", values)
            self._depth = values["data"]["depth"]
            
            self._depth_msg = 'D{:04.1f}'.format(self._depth)
            
        elif values['name'] == 'YXMTW':  # Temperature
            #print("YXMTW", values)
            self._temp = values["data"]["temp"]
            
            self._temp_msg = 'T{:.1f}'.format(self._temp)
            
       # Save record when have all parts            
        if (self._lat is not None) and (self._depth is not None):
            #self.finishLogging()

            # display data
            self._lcd.lcd_display_string(self._lat_msg, 1, 1)
            self._lcd.lcd_display_string(self._depth_msg, 1, 11)
            
            self._lcd.lcd_display_string(self._lon_msg, 2)        
            self._lcd.lcd_display_string(self._temp_msg, 2, 11)

            # clear data for next round of sentences            
            self._lat = None
            self._lon = None
            self._depth = None
            self._temp = None
            
        
def main():    
    ''' Test function for GPS object '''
    print("Testing GPS")
    m = Monitor()

if __name__ == "__main__":
    main()
