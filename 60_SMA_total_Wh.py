#!/usr/bin/python3

import datetime
from influxdb import InfluxDBClient
from SMA import *

sb = SMA()

#sb.id()
#sb.value('productivity_day')
totalWh = sb.value('productivity_total')
#sb.getLogger('txt')
sb.logout()

#----------------------------------
# influx REAL TIME DB LOCATION
ifdb = "energydb"
#ifhost = "192.168.0.177"  #RPI
ifhost = "ASUS"
ifport = 8086
name = "SMA"
#----------------------------------

time = datetime.datetime.utcnow()

ifclient = InfluxDBClient(ifhost,ifport)
ifclient.switch_database(ifdb)

body = [
            {
                "measurement": name,   
                "time": time,
                "fields": {
                    "TotWhOut": totalWh
                    }
            }
        ]

ifclient.write_points(body)

