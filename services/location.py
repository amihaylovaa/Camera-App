import re

import serial


def get_latitude(lat, lat_direction):
    lat_degree = lat[0:2]
    lat_min = lat[2:]

    return lat_degree + '° ' + lat_min + '\' ' + lat_direction


def get_longitude(lon, lon_direction):
    if len(lon) == 7:
        lon_degree = lon[0:2]
        lon_min = lon[2:]
    else:
        lon_degree = lon[0:3]
        lon_min = lon[3:]

    return lon_degree + '° ' + lon_min + '\' ' + lon_direction


def get_date_time(time_gps, date_gps):
    day = (int)(date_gps[0:2])
    month = (int)(date_gps[2:4])
    year = (int)(date_gps[4:])
    hour = (int)(time_gps[0:2])
    minutes =  (int)(time_gps[2:4]) 
    seconds = (int)(time_gps[4:])
    date_time_gps = localtime.localtime(year, month, day, hour, minutes, seconds)
    offset = datetime.timedelta(hours=3)
    
    return date_time_gps + offset


def read_gps_data():
    port = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
    start_tag = 0
    end_tag = 6
    while(1):
     line = port.readline()
     if "$GPRMC" == line[start_tag:end_tag]:
        gprmc_sentence = line[(end_tag + 1):]
        gprmc_sentence_splitted = re.findall("[^,]+", gprmc_sentence)
        validation = gprmc_sentence_splitted[1]
        if validation == 'A'
         lat = gprmc_sentence_splitted[2]
         lat_direction = gprmc_sentence_splitted[3]
         lon = gprmc_sentence_splitted[4]
         lon_direction = gprmc_sentence_splitted[5]
         time_gps = gprmc_sentence_splitted[0]
         date_gps = gprmc_sentence_splitted[8]
         date_time = get_date_time(time_gps, date_gps)
         latitude = get_latitude(lat, lat_direction)
         longitude = get_longitude(lon, lon_direction)

         return "latitude:" + str(latitude) + ", longitude:" + str(longitude) + ", " + str(date_time) + ""
