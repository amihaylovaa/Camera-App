import re
import datetime
import serial 
from flask import Flask
  
app = Flask(__name__)

# TODO - optimization
def read_GPS_data():
  port = serial.Serial('/dev/ttyS0', 9600)
  line = port.readline(1000) 
  start_tag = 0
  end_tag =  6  
  if ("$GPRMC"==line[start_tag:end_tag]): 
    gprmc_line = line[(end_tag+1):]
    gprmc_splitted = re.findall("[^,]+", gprmc_line)
    time_utc = gprmc_splitted[0]
    lat = gprmc_splitted[2]
    lat_direction = gprmc_splitted[3]
    date = gprmc_splitted[8]
    day = (int) (date[0:2])
    month = (int) (date[2:4])
    year = (int) (date[4:])
    hours = (int) (time_utc[0:2])
    minutes = (int) (time_utc[2:4])
    seconds =(int) (time_utc[4:])
    date_time =  datetime.datetime(year,month,day, hours, minutes, seconds)
    lat_degree = (float)(lat[0:2])
    lat_min = ((float)(lat[2:]))/60.0
    latitude=0
    if(lat_direction=='S'):
     latitude = -(lat_degree+lat_min)
    else:
     latitude = lat_degree+lat_min
    lon = gprmc_splitted[4]
    lon_direction = gprmc_splitted[5]
    lon_degree = 0
    lon_min = 0
    longitude=0
    if(len(lon)==7):
     lon_degree = (float)(lon[0:2])
     lon_min = ((float)(lon[2:]))/60
    else:
     lon_degree =(float) (lon[0:3])
     lon_min = ((float)(lon[3:]))/60
    if(lat_direction=='W'):
     longitude = -(lat_degree+lat_min)
    else:
     longitude = lon_degree+lon_min

    return "latitude:"+str(latitude)+", longitude:"+str(longitude)+", "+date_time.strftime('%d/%m/%Y, %H:%M:%S')+""


@app.route("/picture")
def take_picture():
       pass

@app.route("/live-stream")
def start_live_stream():
       pass

@app.route("/video/<date>")
def get_video(date):
       read_GPS_data()

if (__name__=="__main__"):
    app.run()