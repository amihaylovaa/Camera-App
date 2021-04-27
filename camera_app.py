import re
import datetime
import serial 
from flask import Flask
  
app = Flask(__name__)

def read_GPS_data():
  port = serial.Serial('/dev/ttyS0', 9600)

@app.route("/picture")
def take_picture():
       pass

@app.route("/live-stream")
def start_live_stream():
       pass

@app.route("/video/<date>")
def get_video(date):
       pass

if (__name__=="__main__"):
    app.run()