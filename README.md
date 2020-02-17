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
                  [--climb] [--weather] [--addr] [-v] [-a]

CLI GPSD Client

optional arguments:
  -h, --help     show this help message and exit
  --loc          get location as lat/lon pair
  --lat          get latitude in decimal format
  --lon          get longitude in decimal format
  --map          get link to your location on a map
  --alt          get altitude in meters
  --speed        get speed in m/s
  --climb        get climb in m/s
  --weather      get weather at location
  --addr         get address from lat/lon (requires internet)
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

Lat,Lon: (48.4363038, -69.979379213)
Alt: 234.708 m
Speed: 0.0 m/s
Climb: 0.0 m/s
Time (UTC): 2020-02-12T20:09:53.000Z
Address:
123, street , County, State, ZIP, Country

Weather:
     \   /     Clear
      .-.      33 °F
   ― (   ) ―   ↓ 0 mph
      `-’      9 mi
     /   \     0.0 in


View Here: http://www.openstreetmap.org/?mlat=48.4363038&mlon=-69.979379213&zoom=15
```

For terse output, you can limit your check:
```
pi@carbox:~ $ pindrop --alt
248.763
```

For verbose output of a single command, use -v. You can also add multiple flags:
```
pi@carbox:~ $ whereami --alt --loc -v
Altitude: 245.936m
Lat,Lon: (30.436288299, -23.979343698)

```
## Roadmap

- Completely wrap gpsd-py3 options, all functions and variables covered.
- Allow for many output modes (json, csv, nmea, kml)
- Pass interface path as an argument
- daemon mode
- REST API Endpoint logging feature (will work with my other project, [hq](https://github.com/needmorecowbell/hq), in the future)
- HomeAssistant Logging feature
- database logging feature
- ~~geocoding lat/lon to address~~

## Contributions

- Please contribute! If there's an error let me know -- even better if you can fix it :)

- A big thank you to anyone who has helped:
    - [MartijnBraam - gpsd-py3](https://github.com/MartijnBraam/gpsd-py3)

