CONFIG = {
    'period':30, # every number in seconds to check gpsd
    'sqlite_db':'/data/pindrop/pindrop.sqlite',
    'output_dir':"/data/pindrop",
    'output_types' : [
                #     'json',
                     'sqlite',
                  ],
    'exception_period': 2, # seconds to wait before querying the gps again in case of low mode/failed call
    'log_rotation': 60 * 5,  # number in seconds to rotate logs
    'naming_pattern': "%Y-%m-%d_%H:%M:%S", # strftime naming pattern for log timestamp
    'logging': [
         #      "location",
                "longitude",
                "latitude",    
                "altitude",
                "hspeed",
                "vertspeed",
                "climb",
                "track",
         #      "movement",
                "sats",
                "error",
                "timestamp",
         #      "address",

                ]
}
