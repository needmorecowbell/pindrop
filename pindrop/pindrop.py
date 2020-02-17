import gpsd
import requests
from time import sleep
import argparse
from pprint import pprint

def get_address(lat,lon):
    try:
        res= requests.get(f'http://wttr.in/{lat},{lon}')
        addr= res.text[res.text.find("Location")+10:]
        addr = addr[:addr.find("[")]
        return addr
    except Exception as e:
        print(e)
        return None

def get_weather(lat,lon):
    try:
        res= requests.get(f'http://wttr.in/{lat},{lon}?Q0T')
        return res.text
    except Exception as e:
        print(e)
        return None

def main():
    art="""
               *****
              *******
             ***   ***
             ***   ***
              *** ***
               *****
                ***
                 *
    """

    parser = argparse.ArgumentParser(description="CLI GPSD Client")
    parser.add_argument('--loc', help="get location as lat/lon pair", action="store_true")    
    parser.add_argument('--lat', help="get latitude in decimal format", action="store_true")
    parser.add_argument('--lon', help="get longitude in decimal format", action="store_true")
    parser.add_argument('--map', help="get link to your location on a map", action="store_true")
    parser.add_argument('--alt', help="get altitude in meters", action="store_true")
    parser.add_argument('--speed', help="get speed in m/s", action="store_true")
    parser.add_argument('--host', help="host to connect to (default: 127.0.01)", dest="host")
    parser.add_argument('--port', help="port to connect to (default: 2497)", dest="port")
    parser.add_argument('--climb', help="get climb in m/s", action="store_true")
    parser.add_argument('--sats', help="get number of satellites currently visible", action="store_true")
    parser.add_argument('--track', help="get course over ground, degrees from true north", action="store_true")
    parser.add_argument('--movement', help="Get the speed and direction of the current movement", action="store_true")
    parser.add_argument('--vertspeed', help="Get the vertical speed", action="store_true")
    parser.add_argument('--error', help="get error estimates of readings, 95 percent confidence", action="store_true")
    parser.add_argument('--device', help="get gps device information", action="store_true")
    parser.add_argument('--weather', help="get weather at location (requires internet)", action="store_true")
    parser.add_argument('--addr', help="get geocoded address from lat/lon (requires internet)", action="store_true")
    parser.add_argument('-v',"--verbose", help="increase verbosity", action="store_true")
    parser.add_argument('-a',"--all", help="display all location information", action="store_true")
    args= parser.parse_args()

    try:
        if(args.host and args.port is None):
            gpsd.connect(host=args.host)
        elif(args.host and args.port):
            gpsd.connect(host=args.host, port= args.port)
        elif(args.host is None and args.port):
            gpsd.connect(port=args.port)
        else:
            gpsd.connect() # use default, no args supplied
    except Exception as e:
        print("Error: ",e)
        exit()
    
    mode = 0
    pre_red= '\033[91m'
    post_red= '\033[00m'

    while(mode == 0):
        try:
            res = gpsd.get_current()
            mode = res.mode

            if(mode > 1):
                if(args.lat):
                    if(args.verbose):
                        print(pre_red+"Latitude: "+post_red+str(res.lat))
                    else:
                        print(res.lat)
                if(args.lon):
                    if(args.verbose):
                        print(pre_red+"Longitude: "+post_red+str(res.lon))
                    else:
                        print(res.lon)
                if(args.alt):
                    if(args.verbose):
                        print(pre_red+"Alt: "+post_red+str(res.alt)+"m")
                    else:
                        print(res.alt)
                if(args.speed):
                    if(args.verbose):
                        print(pre_red+"Speed: "+post_red+str(res.hspeed)+"m/s")
                    else:
                        print(res.hspeed,"m/s")
                if(args.climb):
                    if(args.verbose):
                        print(pre_red+"Climb: "+post_red+ str(res.climb)+"m/s")
                    else:
                        print(res.climb,"m/s")
                if(args.loc):
                    if(args.verbose):
                        print(pre_red+"Lat,Lon: "+post_red+str(res.position()))
                    else:
                        print(res.position())
                if(args.sats):
                    if(args.verbose):
                        print(pre_red+"Satellites Available: "+post_red+str(res.sats))
                    else:
                        print(res.sats)
                if(args.track):
                    if(args.verbose):
                        print(pre_red+"Track: "+post_red+str(res.track))
                    else:
                        print(res.track)
                if(args.movement):
                    if(args.verbose):
                        print(pre_red+"Movement: "+post_red)
                        pprint(res.movement())
                    else:
                        pprint(res.movement())
                if(args.error):
                    if(args.verbose):
                        print(pre_red+"Percent Error Information: "+post_red)
                        pprint(res.error)
                    else:
                        pprint(res.error)
                if(args.device):
                    if(args.verbose):
                        print(pre_red+"Device Information: "+post_red)
                        pprint(gpsd.device())
                    else:
                        pprint(gpsd.device())

                if(args.vertspeed):
                    if(args.verbose):
                        print(pre_red+"Vertical Speed: "+post_red)
                        pprint(res.speed_vertical())
                    else:
                        pprint(res.speed_vertical())

                if(args.map):
                    if(args.verbose):
                        print(pre_red+"Link to Map: "+post_red+ str(res.map_url()))
                    else:
                        print(res.map_url())

                if(args.weather):
                    if(args.verbose):
                        print(pre_red+'Weather: '+post_red)
                        print(get_weather(res.lat, res.lon))
                    else:
                        print(get_weather(res.lat, res.lon))
                if(args.addr):
                    if(args.verbose):
                        print(pre_red+"Address"+post_red)
                        print(get_address(res.lat,res.lon))
                    else:
                        print(get_address(res.lat, res.lon))

                if(args.all):
                    print(pre_red+art+post_red)
                    print("              Pindrop\n")
                    print(pre_red+"Lat,Lon:"+post_red+str(res.position()))
                    print(pre_red+"Alt: "+post_red+str(res.alt)+"m")
                    print(pre_red+"Speed: "+post_red+str(res.hspeed)+"m/s")
                    print(pre_red+"Vertical Speed: "+post_red+ str(res.speed_vertical())+"m/s")
                    print(pre_red+"Climb: "+post_red+ str(res.climb)+"m/s")
                    print(pre_red+"Track: "+post_red+str(res.track))
                    print(pre_red+"Movement: "+post_red)
                    pprint(res.movement())
                    print(pre_red+"Device Information: "+post_red)
                    pprint(gpsd.device())
                    print(pre_red+"Satellites Available: "+post_red+str(res.sats))
                    print(pre_red+"Mode: "+post_red+ str(res.mode))

                    print(pre_red+"Percent Error Information: "+post_red)
                    pprint(res.error)
                    print(pre_red+"Time (UTC): "+post_red+ str(res.time))
                    address = get_address(res.lat, res.lon)
                    if(address):
                        print(pre_red+"Address: "+post_red)
                        print(address)
                    print()
                    weather =  get_weather(res.lat,res.lon)
                    if(weather):
                        print(pre_red+"Weather: "+post_red)
                        print(weather)
                    print()
                    print(pre_red+"View Here: "+post_red+ res.map_url())
            else:
                sleep(1)
        except Exception as e:
            print(e)
            sleep(1)

if (__name__ == "__main__"):
    main()
