from flask import Flask
from flask import send_file
from flask import Response
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import base64
import re
import datetime
import serial 


app = Flask(__name__)
api = Api(app)
CORS(app)

def get_latitude(lat, lat_direction):
    lat_degree = lat[0:2]
    lat_min = lat[2:]

    return lat_degree+'° '+lat_min+ '\' '+ lat_direction
    
def get_longitude(lon, lon_direction):
    lon_degree = 0
    lon_min = 0

    if(len(lon)==7):
     lon_degree = lon[0:2]
     lon_min = lon[2:]
    else:
     lon_degree = lon[0:3]
     lon_min = lon[3:]
    
     return lon_degree+'° '+lon_min+ '\' '+ lon_direction
    
    
def get_date_time(time_utc, date_gps):
    date = date_gps[0:2] + "-" + date_gps[2:4] + "-"+date_gps[4:]+""
    time = time_utc[0:2] + ":" + time_utc[2:4] + ":"+time_utc[4:]+""

    return date+" "+time
      
def read_GPS_data():
  port = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
  line = port.readline()
  start_tag = 0
  end_tag =  6  
  if ("$GPRMC"==line[start_tag:end_tag]): 
    gprmc_line = line[(end_tag+1):]
    gprmc_splitted = re.findall("[^,]+", gprmc_line)
    time_utc = gprmc_splitted[0]
    lat = gprmc_splitted[2]
    lat_direction = gprmc_splitted[3]
    lon = gprmc_splitted[4]
    lon_direction = gprmc_splitted[5]
    date_gps = gprmc_splitted[8]
    date_time = get_date_time(time_utc, date_gps)
    latitude = get_latitude(lat, lat_direction) 
    longitude = get_longitude(lon, lon_direction) 

    return "latitude:"+str(latitude)+", longitude:"+str(longitude)+", "+date_time+""

class Picture(Resource):
    def get(self):
        pass

class LiveStream(Resource):
    def get(self):
        pass

class Video(Resource):
    def get(self, date):
        pass

api.add_resource(Picture, "/picture")
api.add_resource(LiveStream, "/live-stream")
api.add_resource(Video, "/video/<string:date>")

if (__name__=="__main__"):
    app.run(debug=True)