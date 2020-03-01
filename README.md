## pindrop

<p align="center">
    <img src="https://user-images.githubusercontent.com/7833164/74372681-10822d80-4da9-11ea-9674-10727f35971b.gif"></img>
</p>

## Requirements

- gpsd
- [gps dongle](https://www.amazon.com/GlobalSat-BU-353-S4-USB-Receiver-Black/dp/B008200LHW)


## Setup

I'm using this tool in an old vehicle to track it's location. However, it can be used for many applications! This is just a command line wrapper for the gpsd-py3 library, which in effect is a gpsd client library. Gpsd is the server that is handling the serial communication from the modem, and will still have to be set as such. There are plenty of tutorials to set up gpsd, [here](https://gpsd.gitlab.io/gpsd/installation.html) is one that I find useful.

Once gpsd is successfully set up, install pindrop's dependencies.

Install with pip: `pip3 install gpsd-pindrop`

or

Clone this reposiitory and run: `pip3 install -r requirements.txt`

## Operation

```
usage: pindrop.py [-h] [--loc] [--lat] [--lon] [--daemon] [--conf CONF]
                  [--map] [--alt] [--speed] [--host HOST] [--port PORT]
                  [--climb] [--sats] [--track] [--movement] [--vertspeed]
                  [--error] [--device] [--weather] [--addr] [-v] [-a]

CLI GPSD Client

optional arguments:
  -h, --help     show this help message and exit
  --loc          get location as lat/lon pair
  --lat          get latitude in decimal format
  --lon          get longitude in decimal format
  --daemon       use daemon mode
  --conf CONF    config for daemon mode
  --map          get link to your location on a map
  --alt          get altitude in meters
  --speed        get speed in m/s
  --host HOST    host to connect to (default: 127.0.0.1)
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
     display all location information
```

## Daemon Mode

By using the --daemon flag, you can use this tool to regularly query and store information from gpsd. Use config.json stored in the root level of this repo as a template. Passing a config is required.


**Example**

```
pi@carbox:~ $ pindrop --daemon --conf /path/to/config.json
```



**Default Configuration**

These are the options by default, which should be replaced with custom config if needed. Options in logging list and output_types should be removed if not needed.

*Remove all comments before using*
```python
{
    'period': 30 # every number in seconds to check gpsd
    'sqlite_db':'/data/pindrop/pindrop.sqlite', #path for sqlite file
    'output_dir':"/data/pindrop", # data directory
    'output_types' : [
                     'json',
                     'sqlite',
                     'kml'
                  ],
    'kml_line_mode': false, #connect the logged points as a linestring in the kml file, if included in output types
    'exception_period': 2, # seconds to wait before querying the gps again in case of low mode/failed call
    'naming_pattern': "%Y%m%d", # strftime naming pattern, sets how often files rotate
    'logging': [            # Possible Options
               "location",
                "longitude",
                "latitude",
                "altitude",
                "hspeed",
                "vertspeed",
                "climb",
                "track",
                "movement",
                "sats",
                "error",
                "timestamp",
                "address",
                ]
}
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

For terse output, omit the verbose flag and call arguments individually:
```
pi@carbox:~ $ pindrop --lat
30.337453049
```

## Roadmap

- ~~Completely wrap gpsd-py3 options, all functions and variables covered.~~
- Allow for many output modes (~~json~~, csv, nmea, ~~kml~~)
- ~~daemon mode~~
- REST API Endpoint logging feature (will work with my other project, [hq](https://github.com/needmorecowbell/hq), in the future)
- HomeAssistant Logging feature
- database logging feature (~~sqlite~~, postgres, mysql)
- ~~geocoding lat/lon to address~~

## Tips

In my case, I want to develop on my main machine, but still use the gpsd server on my raspberry pi for getting information. I make an ssh tunnel for port 2497 on the pi with the gpsd server, and then I can develop as if the server was local:

`ssh -N -L 2947:localhost:2947 pi@10.0.0.17`

You can also change the settings of gpsd to make the port accessible to other devices, but this is a more secure option that leaves gpsd untouched.

## Contributions

- Please contribute! If there's an error let me know -- even better if you can fix it :)

- A big thank you to anyone who has helped:
    - [MartijnBraam - gpsd-py3](https://github.com/MartijnBraam/gpsd-py3)

