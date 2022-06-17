import client_config
import time
from picamera import PiCamera
import uuid


class Capture:
    def __init__(self):
        self.files = []

    def record_video(self, capture_duration=10):
        pass
        # vid_path = client_config.video_dir + 'vid' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.mp4'
        # out = cv2.VideoWriter(vid_path, fourcc, 20.0, (640, 480))
        #
        # start_time1 = time.time()
        # while int(time.time() - start_time1) < capture_duration:
        #     ret, frame = cap.read()
        #     if ret:
        #         frame = cv2.flip(frame, 90)
        #         out.write(frame)
        #         img_path = client_config.image_dir + 'img' + datetime.datetime.now().strftime(
        #             "%Y-%m-%d_%H-%M-%S") + '.jpg'
        #         cv2.imwrite(img_path, frame)
        #         self.files.append([img_path, "image"])
        #     else:
        #         break
        # self.files.append([vid_path, "video"])
        # self.save_to_db()

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
