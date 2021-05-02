from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from resources.live_stream import LiveStream
from resources.picture import Picture
from resources.video import Video

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(Picture, "/picture")
api.add_resource(LiveStream, "/live-stream")
api.add_resource(Video, "/video/<string:date>")

if __name__ == "__main__":
    app.run(debug=True)
