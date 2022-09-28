import config
import time
from picamera import PiCamera
import uuid
from subprocess import call

# paths
video_dir = config.base_dir+"/multimedia/videos/"
database_path = config.base_dir+"/multimedia/database.sqlite"


class Capture:
    def __init__(self):
        self.files = []
        self.camera = None

    def change_format(self, file_path):
        new_file_path = file_path
        if file_path.endswith(".h264"):
            new_file_path = file_path[:-5]+".mp4"
            call("MP4Box -fps 30 -add "+file_path+" "+new_file_path, shell=True)
            call("rm "+file_path, shell=True)

        return new_file_path

    def record_video(self, capture_duration=10):
        self.init_camera()
        vid_path = video_dir + 'vid' + uuid.uuid4().__str__() + '.h264'
        self.camera.start_recording(vid_path)
        self.camera.wait_recording(capture_duration)
        self.camera.stop_recording()
        self.files.append([self.change_format(vid_path), "video"])
        self.save_to_db()

    def init_camera(self):
        if self.camera is None:
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)

    def save_to_db(self):
        pass
