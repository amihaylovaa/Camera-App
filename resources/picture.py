import base64
import cv2
from flask import make_response
from flask_restful import Resource, abort

from services.camera import Camera, store_frame


class Picture(Resource):
    def __init__(self):
        self.cam = Camera()

    def post(self):
        captured, frame = self.cam.capture_frame()
        if not captured:
            abort(500, description="Capturing frame failed")

        stored = store_frame(frame)
        if not stored:
            abort(500, description="Storing image failed")

        encoded, image = cv2.imencode('.jpg', frame)
        if not encoded:
            abort(500, description="Encoding image failed")

        response = make_response(base64.b64encode(image.tobytes()))

        return response
