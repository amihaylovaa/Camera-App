import base64

from flask import Flask, Response
from flask_cors import CORS
from flask_restful import abort

from services.camera import Camera

app = Flask(__name__)
CORS(app)


@app.route('/picture', methods=['POST'])
def picture():
    try:
        frame = Camera().get_frame()
    except RuntimeError as err:
        abort(500, description=err.__str__())

    # TODO: Fix image storing
    # stored = store_frame(frame)

    return Response(base64.b64encode(frame))


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/live_stream')
def live_stream():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video')
def video():
    pass


if __name__ == "__main__":
    app.run()
