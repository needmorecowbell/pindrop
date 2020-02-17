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
                if(args.weather):
                    print(get_weather(res.lat, res.lon))
                if(args.addr):
                    print(get_address(res.lat, res.lon))
                if(args.all):
                    print("\033[91m"+art+"\033[00m")
                    print("              Pindrop\n")
                    print("\033[91m"+"Lat,Lon:"+"\033[00m"+str(res.position()))
                    print("\033[91m"+"Alt: "+"\033[00m"+str(res.alt)+"m")
                    print("\033[91m"+"Speed: "+"\033[00m"+str(res.hspeed)+"m/s")
                    print("\033[91m"+"Climb: "+"\033[00m"+ str(res.climb)+"m/s")
                    print("\033[91m"+"Time (UTC): "+"\033[00m"+ str(res.time))
                    address = get_address(res.lat, res.lon)
                    if(address):
                        print("\033[91m"+"Address: "+"\033[00m\n"+ address)
                    print()
                    weather =  get_weather(res.lat,res.lon)
                    if(weather):
                        print("\033[91m"+"Weather: "+"\033[00m\n"+ weather)
                    print()
                    print("\033[91m"+"View Here: "+"\033[00m"+ res.map_url())
            else:
                sleep(1)
        except Exception as e:
            print(e)
            sleep(1)

if (__name__ == "__main__"):
    main()
