import gpsd
from time import sleep
import argparse

if (__name__ == "__main__"):
    art="""
               *****
              *******
             ***   ***
             ***   ***
              *** ***
               *****
                ***
                 *
            Where Am I?
    """

    parser = argparse.ArgumentParser(description="GPSD CLI Client")
    parser.add_argument('--loc', help="get location as lat/lon pair", action="store_true")    
    parser.add_argument('--lat', help="get latitude in decimal format", action="store_true")
    parser.add_argument('--lon', help="get longitude in decimal format", action="store_true")
    parser.add_argument('--map', help="get link to your location on a map", action="store_true")
    parser.add_argument('--alt', help="get altitude in meters", action="store_true")
    parser.add_argument('--speed', help="get speed in m/s", action="store_true")
    parser.add_argument('--climb', help="get climb in m/s", action="store_true")
    parser.add_argument('-v',"--verbose", help="increase verbosity", action="store_true")
    parser.add_argument('-a',"--all", help="display all location information", action="store_true")
    args= parser.parse_args()
    gpsd.connect()
    mode = 0

    while(mode == 0):
        try:
            res = gpsd.get_current()
            mode = res.mode

            if(mode > 1):
                if(args.lat):
                    if(args.verbose):
                        print(f"Latitude: {res.lat}")
                    else:
                        print(res.lat)
                if(args.lon):
                    if(args.verbose):
                        print(f"Longitude: {res.lon}")
                    else:
                        print(res.lon)
                if(args.alt):
                    if(args.verbose):
                        print(f"Altitude: {res.alt}m")
                    else:
                        print(res.alt)
                if(args.speed):
                    if(args.verbose):
                        print(f"Speed: {res.hspeed}m/s")
                    else:
                        print(res.hspeed,"m/s")

                if(args.climb):
                    if(args.verbose):
                        print(f"Climb: {res.climb}m/s")
                    else:
                        print(res.climb,"m/s")

                if(args.loc):
                    if(args.verbose):
                        print(f"Lat,Lon: {res.position()}")
                    else:
                        print(res.position())

                if(args.map):
                    print(f"View Here: {res.map_url()}")

                if(args.all):
                    print(art)
                    print(f"Lat,Lon: {res.position()}")
                    print(f"Alt: {res.alt} m")
                    print(f"Speed: {res.hspeed} m/s")
                    print(f"Climb: {res.climb} m/s")
                    print(f"Time (UTC): {res.time}")
                    print()
                    print(f"View Here: {res.map_url()}")
            else:
                sleep(1)
        except Exception as e:
            print(e)
            sleep(1)
