import client_config
import time
from picamera import PiCamera
import uuid


class Capture:
    def __init__(self):
        self.files = []

    def record_video(self, capture_duration=10):
        camera = PiCamera()
        vid_path = client_config.video_dir + 'vid' + uuid.uuid4().__str__() + '.h264'
        camera.start_recording(vid_path)
        camera.wait_recording(capture_duration)
        camera.stop_recording()
        self.files.append([vid_path, "video"])
        self.save_to_db()

    def record_audio(self, record_seconds=10):
        pass

    def snap(self, num=1):
        camera = PiCamera()
        time.sleep(2)
        for i in range(num):
            img_path = client_config.image_dir + 'img' + uuid.uuid4().__str__() + '.jpg'
            camera.capture(img_path)
            self.files.append([img_path, "image"])
        self.save_to_db()

    def save_to_db(self):
        pass
