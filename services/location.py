import datetime

import serial


class Location:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)

        return cls._instance

    def __init__(self):
        self.port = serial.Serial('/dev/ttyS0', 115200)
        self.sentence_type = "$GNRMC"
        self.sentence_size = 1100
        self.template = "Latitude: {} Longitude: {} Time: {}"

    def read_gps_data(self):
        data = self.port.read(self.sentence_size)
        for line in data.decode().splitlines():
            if line.startswith(self.sentence_type):
                elements = line.split(",")
                validation = elements[2]
                if validation is 'V':
                    continue

                lat = elements[3]
                lat_direction = elements[4]
                lon = elements[5]
                lon_direction = elements[6]
                time = elements[1]
                date = elements[9]
                date_time = get_date_time(time, date)
                latitude = get_latitude(lat, lat_direction)
                longitude = get_longitude(lon, lon_direction)

                return self.template.format(latitude, longitude, date_time)

        return self.template.format("N/A", "N/A", "N/A")


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


def get_date_time(time, date):
    day = int(date[0:2])
    month = int(date[2:4])
    year = int(date[4:])
    hour = int(time[0:2])
    minutes = int(time[2:4])
    seconds = int(time[4:6])
    timestamp = datetime.datetime(year, month, day, hour, minutes, seconds)
    offset = datetime.timedelta(hours=3)

    return timestamp + offset
