# Sonar-GPS
This is code to support a GPS/Sonar unit that records GPS information (time, lat, long) and sonar data (depth, temperature).
The system consists of:
* GPS unit (cheap USB GPS)
* Sonar [AirMar DT800](https://www.airmar.com/productdescription.html?id=109)
* Raspberry Pi computer 
* [Screen](https://www.amazon.com/gp/product/B07D83DY17/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)



Both the GPS and sonar output standard [NMEA](https://www.nmea.org/) sentences, whith the code collects, parses and stores.

Data is recorded to a csv file with the following format:

Time, Latitude, Longitude, Depth, Temperature

2021-07-22 13:27:56, 39.080554, -86.430522, 3.8, None

The data is usually post-processed to convert depth to altitude (with adjustment for current lake level).  For Lake Monroe (main site of study), the standard pool is 538 ft, and depths are adjusted relative to this elevation.

A transformer directly powers the sonar, and drops the power to 3V for the Raspberry Pi
The sonar is housed in a length of 4" PVC pipe, with a flat cap on the bottom through which the transducer is mounted.  The top cap is removeable.  The top cap has a hole through which the transducer cable exits, and has a washer glued to it for mounting the magnetic GPS.  The pipe bolts to several PVC 3/4" pipe fittings that allow the unit to be mounted on different vehicles (ie kayaks).

![Electronics](https://user-images.githubusercontent.com/24879035/126697631-98894553-2123-45f0-b8e9-c0155e78da5e.jpg)


