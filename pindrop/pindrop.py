import gpsd
import requests
from time import sleep
import argparse

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

    parser.add_argument('--climb', help="get climb in m/s", action="store_true")

    parser.add_argument('--weather', help="get weather at location", action="store_true")
    parser.add_argument('--addr', help="get address from lat/lon (requires internet)", action="store_true")
    parser.add_argument('-v',"--verbose", help="increase verbosity", action="store_true")
    parser.add_argument('-a',"--all", help="display all location information", action="store_true")
    args= parser.parse_args()

    try:
        gpsd.connect(host="127.0.0.1", port=2947)
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
                        print(pre_red+"Lat,Lon:"+post_red+str(res.position()))
                    else:
                        print(res.position())

                if(args.map):
                    print(f"View Here: {res.map_url()}")
                if(args.weather):
                    print(get_weather(res.lat, res.lon))
                if(args.addr):
                    print(get_address(res.lat, res.lon))
                if(args.all):
                    print(pre_red+art+post_red)
                    print("              Pindrop\n")
                    print(pre_red+"Lat,Lon:"+post_red+str(res.position()))
                    print(pre_red+"Alt: "+post_red+str(res.alt)+"m")
                    print(pre_red+"Speed: "+post_red+str(res.hspeed)+"m/s")
                    print(pre_red+"Climb: "+post_red+ str(res.climb)+"m/s")
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
