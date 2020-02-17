## pindrop

<p align="center">
    <img src="https://user-images.githubusercontent.com/7833164/74372681-10822d80-4da9-11ea-9674-10727f35971b.gif"></img>
</p>

## Requirements 

- gpsd
- [gps dongle](https://www.amazon.com/GlobalSat-BU-353-S4-USB-Receiver-Black/dp/B008200LHW)


## Setup

I'm using this tool in an old vehicle to track it's location. However, it can be used for many applications! This is just a command line wrapper for the gpsd-py3 library, which in effect is a gpsd client library. Gpsd is the server that is handling the serial communication from the modem, and will still have to be set as such. There are plenty of tutorials to set up gpsd, [here](https://gpsd.gitlab.io/gpsd/installation.html) is one that I find useful.

Once gpsd is successfully set up, install whereami's dependencies.

Install with pip
`pip3 install gpsd-pindrop`

or

Clone this reposiitory and run: 
`pip3 install -r requirements.txt`

## Operation

```
usage: pindrop.py [-h] [--loc] [--lat] [--lon] [--map] [--alt] [--speed]
                  [--host HOST] [--port PORT] [--climb] [--sats] [--track]
                  [--movement] [--vertspeed] [--error] [--device] [--weather]
                  [--addr] [-v] [-a]

CLI GPSD Client

optional arguments:
  -h, --help     show this help message and exit
  --loc          get location as lat/lon pair
  --lat          get latitude in decimal format
  --lon          get longitude in decimal format
  --map          get link to your location on a map
  --alt          get altitude in meters
  --speed        get speed in m/s
  --host HOST    host to connect to (default: 127.0.01)
  --port PORT    port to connect to (default: 2497)
  --climb        get climb in m/s
  --sats         get number of satellites currently visible
  --track        get course over ground, degrees from true north
  --movement     Get the speed and direction of the current movement
  --vertspeed    Get the vertical speed
  --error        get error estimates of readings, 95 percent confidence
  --device       get gps device information
  --weather      get weather at location (requires internet)
  --addr         get geocoded address from lat/lon (requires internet)
  -v, --verbose  increase verbosity
  -a, --all      display all location information
```

## Example output:

For all possible output printed in a nice way, use the -a flag for all output
```
pi@carbox:~ $ pindrop -a

               *****
              *******
             ***   ***
             ***   ***
              *** ***
               *****
                ***
                 *

              Pindrop

Lat,Lon:(30.337453049, -70.113382638)
Alt: 285.318m
Speed: 0.0m/s
Vertical Speed: 0m/s
Climb: 0.0m/s
Track: 0.0
Movement:
{'climb': 0.0, 'speed': 0.0, 'track': 0.0}
Device Information:
{'driver': 'SiRF', 'path': '/dev/ttyUSB0', 'speed': 4800}
Satellites Available: 12
Mode: 3
Percent Error Information:
{'c': 0.68, 's': 0.26, 't': 0.005, 'v': 29.011, 'x': 9.174, 'y': 11.076}
Time (UTC): 2020-02-17T16:16:43.000Z
Address:
123, Street, Town, County, State, Zip, Country

Weather:
               Mist
  _ - _ - _ -  33 °F
   _ - _ - _   ↓ 0 mph
  _ - _ - _ -  3 mi
               0.0 in


View Here: http://www.openstreetmap.org/?mlat=30.337453009&mlon=-70.113382638&zoom=15
```
## Roadmap

- ~~Completely wrap gpsd-py3 options, all functions and variables covered.~~
- Allow for many output modes (json, csv, nmea, kml)
- daemon mode
- REST API Endpoint logging feature (will work with my other project, [hq](https://github.com/needmorecowbell/hq), in the future)
- HomeAssistant Logging feature
- database logging feature
- ~~geocoding lat/lon to address~~

## Contributions

- Please contribute! If there's an error let me know -- even better if you can fix it :)

- A big thank you to anyone who has helped:
    - [MartijnBraam - gpsd-py3](https://github.com/MartijnBraam/gpsd-py3)

