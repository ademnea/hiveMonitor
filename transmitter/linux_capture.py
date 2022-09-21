import cv2
import pyaudio
import wave
import time
import uuid
import config

# paths
video_dir = config.base_dir+"/multimedia/videos/"
audio_dir = config.base_dir+"/multimedia/audios/"
image_dir = config.base_dir+"/multimedia/images/"
database_path = config.base_dir+"/multimedia/database.sqlite"


class Capture:
    def __init__(self):
        self.files = []

    def record_video(self, capture_duration=10):
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        vid_path = video_dir + 'vid' + uuid.uuid4().__str__() + '.mp4'
        out = cv2.VideoWriter(vid_path, fourcc, 20.0, (640, 480))

        start_time1 = time.time()
        while int(time.time() - start_time1) < capture_duration:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 90)
                out.write(frame)
                img_path = image_dir + 'img' + uuid.uuid4().__str__() + '.jpg'
                cv2.imwrite(img_path, frame)
                self.files.append([img_path, "image"])
            else:
                break
        self.files.append([vid_path, "video"])

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        self.save_to_db()

    def record_audio(self, record_seconds=10):
        chunk = 1024
        form = pyaudio.paInt16
        channels = 2
        rate = 44100

        p = pyaudio.PyAudio()

        stream = p.open(format=form,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

        frames = []

        for i in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()
        aud_path = audio_dir + 'aud' + uuid.uuid4().__str__() + '.wav'
        wf = wave.open(aud_path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(form))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        self.files.append([aud_path, "audio"])
        self.save_to_db()

    def snap(self, num):
        pass

    def save_to_db(self):
        pass
