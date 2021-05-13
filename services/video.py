import threading
import time

import cv2

from services.camera import CameraEvent


class Video:
    name = ''
    frame = None  # current frame stored by background thread
    last_access = 0  # timestamp of last client access to the camera

    event = CameraEvent()

    def __init__(self, file_name):
        Video.name = file_name

        """Start video playback thread."""
        Video.last_access = time.time()

        # Start background frame thread.
        Video.background_thread = threading.Thread(target=self._thread)
        Video.background_thread.start()

        # Wait until frames are available.
        while Video.get_frame() is None:
            time.sleep(0)

    @staticmethod
    def frames():
        cap = cv2.VideoCapture(Video.name)
        cap.open(Video.name)
        while cap.IsOpened():
            captured, frame = cap.read()

            encoded, image = cv2.imencode('.jpg', frame)
            if not encoded:
                raise RuntimeError('Could not encode frame.')

            yield image.tobytes()

    @staticmethod
    def get_frame():
        """Return the current camera frame."""
        Video.last_access = time.time()

        # Wait for a signal from the camera thread.
        Video.event.wait()
        Video.event.clear()

        return Video.frame

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')

        frames_iterator = cls.frames()
        for frame in frames_iterator:
            Video.frame = frame
            Video.event.set()  # send signal to clients

            # Stop the background thread if a client has not requested frames within the last 10 seconds.
            if time.time() - Video.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break

        Video.background_thread = None
