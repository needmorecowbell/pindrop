import gpsd
import requests
from time import sleep
import argparse
from pprint import pprint
import json
import socket
import datetime
import json
import sqlite3
import simplekml


def is_internet_available(hostname='google.com'):
  try:
    host = socket.gethostbyname(hostname)
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except:
     pass
  return False

def get_address(lat,lon):
    try:
        res= requests.get(f'http://wttr.in/{lat},{lon}', timeout=3)
        addr= res.text[res.text.find("Location")+10:]
        addr = addr[:addr.find("[")]
        return addr
    except Exception as e:
        print(e)
        return None

def get_weather(lat,lon):
    try:
        res= requests.get(f'http://wttr.in/{lat},{lon}?Q0T', timeout=3)
        return res.text
    except Exception as e:
        print(e)
        return None

def _parse_args(parser):
    parser.add_argument('--loc', help="get location as lat/lon pair", action="store_true")
    parser.add_argument('--lat', help="get latitude in decimal format", action="store_true")
    parser.add_argument('--lon', help="get longitude in decimal format", action="store_true")
    parser.add_argument('--daemon', help="use daemon mode", action="store_true")
    parser.add_argument('--conf', help="config for daemon mode", dest="conf")
    parser.add_argument('--map', help="get link to your location on a map", action="store_true")
    parser.add_argument('--alt', help="get altitude in meters", action="store_true")
    parser.add_argument('--speed', help="get speed in m/s", action="store_true")
    parser.add_argument('--host', help="host to connect to (default: 127.0.0.1)", dest="host")
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


def daemon_mode(config):
    if(config['output_dir'][-1] is not '/'):
        config['output_dir']= config['output_dir']+'/'
    if(config['sqlite_db_dir'][-1] is not '/'):
        config['sqlite_db_dir']= config['sqlite_db_dir']+'/'
    kml = None
    
    if('kml' in config['output_types']):
        kml = simplekml.Kml() # start a new kml file at the beginning of daemon mode
        if(config['kml_line_mode']):
            kml_line= kml.newlinestring()
        else:
            kml_line=None
    while(True):
        mode = 0
        while(mode <= 1): # keep going until you find a signal
            try:
                gpsd.connect()
                res = gpsd.get_current()
                mode = res.mode
                logging = config['logging']
                results= {}
                if(mode > 1):
                    if("location" in logging):
                        results['location'] = str(res.position())
                    if("longitude" in logging):
                        results['longitude'] = res.lon
                    if("latitude" in logging):
                        results['latitude'] = res.lat
                    if('altitude' in logging):
                        results['altitude'] = res.alt
                    if('hspeed' in logging):
                        results['hspeed'] = res.hspeed
                    if('vertspeed' in logging):
                        results['vertspeed'] = res.speed_vertical()
                    if('climb' in logging):
                        results['climb'] =  res.climb
                    if('track' in logging):
                        results['track'] = res.track
                    if('movement' in logging):
                        results['movement'] = "".join(str(res.movement()))
                    if('sats' in logging):
                        results['sats'] = res.sats
                    if('error' in logging):
                        results['error'] = "".join(str(res.error))
                    if('timestamp' in logging):
                        results['timestamp'] = res.time
                    if(is_internet_available()):
                        # only available with internet connectivity
                        if('address' in logging):
                            results['address'] = get_address(res.lat, res.lon)

                    print(results)
                    log_results(results, config, kml, kml_fname=None, kml_line=kml_line)
                    sleep(config["period"])

                else: # call failed, try again
                    sleep(config['exception_period'])
            except Exception as e:
                print(e)
                sleep(config['exception_period'])

def log_results(results, config, kml=None, kml_fname=None, kml_line=None):
    if('json' in config['output_types']):
        full_path= config['output_dir']+datetime.datetime.utcnow().strftime(config['naming_pattern'])+".json"
        try:
            with open(full_path,'w') as fp:
                json.dump(results, fp)
        except Exception as e:
            print("Error: ",e)

    if('sqlite' in config['output_types']):
        print("Writing to sqlite")
        print(config['sqlite_db_dir']+datetime.datetime.utcnow().strftime(config['naming_pattern'])+'.sqlite')
        create_sqlite_table(config['sqlite_db_dir']+datetime.datetime.utcnow().strftime(config['naming_pattern'])+'.sqlite')
        log_to_sqlite(results, config)
        print("finished logging")
    if('kml' in config['output_types']):
        print("Adding point to kml")
        if(config['kml_line_mode']):
            kml_line.coords.addcoordinates([(results["longitude"], results['latitude'], results['altitude'])])
        else:
            pnt = kml.newpoint(name=results["timestamp"], coords=[(results["longitude"], results['latitude'])], description=str(results))
        if(kml_fname):
            kml.save(kml_fname) # save after each time
        else:
            kml.save(config['output_dir']+datetime.datetime.utcnow().strftime(config['naming_pattern'])+'.kml')


def create_sqlite_table(db_file=None):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        sql_create_pindrop_table = """ CREATE TABLE IF NOT EXISTS pindrop (
                                            id integer PRIMARY KEY,
                                            latitude text,
                                            longitude text,
                                            altitude real,
                                            hspeed real,
                                            vertspeed real,
                                            climb real,
                                            track real,
                                            movement text,
                                            location text,
                                            sats int,
                                            error text,
                                            timestamp text,
                                            address text,
                                            weather text
                                        ); """
        conn.execute(sql_create_pindrop_table)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()

def log_to_sqlite(results, config, user=None, pswd=None,host=None):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        print(config['sqlite_db_dir']+datetime.datetime.utcnow().strftime(config['naming_pattern'])+'.sqlite')
        conn = sqlite3.connect(config['sqlite_db_dir']+datetime.datetime.utcnow().strftime(config['naming_pattern'])+'.sqlite')
        cur= conn.cursor()
        insert_params= str(config['logging']).replace('[','').replace(']','')
        insert_values= ''
        for x in range(0,len(results.values())):
            insert_values+="?,"
        insert_values = insert_values[:-1]
        query = f"INSERT INTO pindrop ({insert_params}) VALUES ({insert_values});"
        print(query)
        cur.execute(query, tuple(list(results.values())))
        conn.commit()
    except Exception as e:
        print("ERROR: ",e)
    finally:
        if conn:
            conn.close()

def _handle_cli_args(args, res):
    pre_red= '\033[91m'
    post_red= '\033[00m'

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

def main():
    parser = argparse.ArgumentParser(description="CLI GPSD Client")
    _parse_args(parser)
    args= parser.parse_args()

    if(args.daemon):
        config= None
        if(args.conf):
            try:
                with open(args.conf, 'r') as fp:
                    config = json.load(fp)
            except Exception as e:
                print("ERROR: ",e)
                exit()
            print("Entering Daemon Mode")
            daemon_mode(config)
        else:
            print("Must provide config with --conf")
            exit()
    else: #using the tool as a cli tool
        # Attempt to make connection to GPSD Server
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
        while(mode <= 1): # keep going until you find a signal
            try:
                res = gpsd.get_current()
                mode = res.mode
                if(mode > 1):
                    _handle_cli_args(args, res)
                else:
                    sleep(1)
            except Exception as e:
                print(e)
                sleep(1)

if (__name__ == "__main__"):
    main()
