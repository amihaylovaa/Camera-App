import base64
import os
from flask import Flask, Response, render_template
from flask_cors import CORS
from flask_restful import abort

from services.camera import Camera

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def load_main_page():
    return render_template('index.html')

@app.route('/picture', methods=['GET'])
def picture():
    try:
        frame = Camera().get_frame()
    except RuntimeError as err:
        abort(500, description=err.__str__())

    # TODO: Fix image storing
    # stored = store_frame(frame)
    frame_encoded = base64.b64encode(frame).decode()

    return render_template("picture.html", frame=frame_encoded)

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/stream', methods=['GET'])
def render_live_stream_template():

    return render_template("stream.html")

@app.route('/live-stream', methods=['GET'])
def start_live_stream():

    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video/<date>')
def video(date):
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files_names = []

    for f in files:
        if(f.startswith(date)):
         files_names.append(f)
    
    return render_template("video.html", files = files_names)
  
@app.route('/<file_name>')
def show_video(file_name):

    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
 
if __name__ == "__main__":
    app.run()