import config
import time
from picamera import PiCamera
import uuid
from subprocess import call

# paths
image_dir = config.base_dir+"/multimedia/images/"
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

    def init_camera(self):
        if self.camera is None:
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)

    def snap(self, num=1):
        self.init_camera()
        time.sleep(2)
        for i in range(num):
            img_path = image_dir + 'img' + uuid.uuid4().__str__() + '.jpg'
            self.camera.capture(img_path)
            self.files.append([self.change_format(img_path), "image"])
        self.save_to_db()

    def save_to_db(self):
        pass
