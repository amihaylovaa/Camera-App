import threading
import time
from _thread import get_ident
from datetime import datetime

import cv2

from services.location import Location


def store_frame(frame):
    ts = int(time.time())
    filename = "{}.jpg".format(ts)

    return cv2.imwrite(filename, frame)


class CameraEvent:
    """An Event-like class that signals all active clients when a new frame is available."""

    def __init__(self):
        # Maps thread ID to a pair of threading event and timestamp.
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        thread_id = get_ident()

        if thread_id not in self.events:
            # Register new client.
            self.events[thread_id] = [threading.Event(), time.time()]

        return self.events[thread_id][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()

        for thread_id, event in list(self.events.items()):
            if not event[0].isSet():
                # Update the client's event if unset.
                event[0].set()
                event[1] = now
            else:
                # Client's event being already set means the client has not processed a previous frame.
                # If the previous frame has stayed for more than 5 seconds, assume the client is gone and remove it.
                if now - event[1] > 5:
                    del self.events[thread_id]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        thread_id = get_ident()
        self.events[thread_id][0].clear()


class Camera:
    background_thread = None  # reads frames from camera
    frame = None  # current frame stored by background thread
    last_access = 0  # timestamp of last client access to the camera

    fourcc = None
    video_writer = None

    event = CameraEvent()

    def __init__(self, picture_request):
        """Start the background camera thread if it isn't running yet."""
        if Camera.background_thread is None:
            Camera.last_access = time.time()

            # Start background frame thread.
            Camera.background_thread = threading.Thread(target=self._thread)
            Camera.background_thread.start()

            # Wait until frames are available.
            while Camera.get_frame() is None:
                time.sleep(0)

            Camera.fourcc = cv2.VideoWriter_fourcc(*'MP4V')

        if not picture_request and Camera.video_writer is None:
            Camera.video_writer = cv2.VideoWriter(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '.mp4', Camera.fourcc,
                                                  20.0, (640, 480))

    @staticmethod
    def get_frame():
        """Return the current camera frame."""
        Camera.last_access = time.time()

        # Wait for a signal from the camera thread.
        Camera.event.wait()
        Camera.event.clear()

        return Camera.frame

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # Read and encode current frame from camera.
            captured, frame = camera.read()
            if not captured:
                raise RuntimeError('Could not capture frame.')

            # Embed location data within the frame.
            cv2.putText(frame, Location().read_gps_data(), (10, 25), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255))

            if Camera.video_writer is not None:
                Camera.video_writer.write(frame)

            encoded, image = cv2.imencode('.jpg', frame)
            if not encoded:
                raise RuntimeError('Could not encode frame.')

            yield image.tobytes()

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')

        frames_iterator = cls.frames()
        for frame in frames_iterator:
            Camera.frame = frame
            Camera.event.set()  # send signal to clients

            # Stop the background thread if a client has not requested frames within the last 10 seconds.
            if time.time() - Camera.last_access > 10:
                frames_iterator.close()

                if Camera.video_writer is not None:
                    Camera.video_writer.release()

                print('Stopping camera thread due to inactivity.')
                break

        Camera.background_thread = None
        Camera.video_writer = None
