from os import path, mkdir
from hashlib import md5
import sqlite3
import cv2
import time
import datetime
import pyaudio
import wave
import client_config


def recursive_mkdir(given_path):
    directories = given_path.split("/")
    length = len(directories)
    given_path, start_index = ("/" + directories[1], 2) if given_path[0] == '/' else (directories[0], 1)
    if not path.isdir(given_path):
        mkdir(given_path)

    for index in range(start_index, length):
        if len(directories[index]) > 0:
            given_path = given_path + '/' + directories[index]
            if not path.isdir(given_path):
                mkdir(given_path)


class Capture:
    files = []

    def __init__(self):
        last_slash = client_config.database_path.rindex('/')
        database_directory = client_config.database_path[0:last_slash]

        # check if directories exist and if not create them
        if not path.isdir(client_config.video_dir):
            recursive_mkdir(client_config.video_dir)
        if not path.isdir(client_config.audio_dir):
            recursive_mkdir(client_config.audio_dir)
        if not path.isdir(client_config.image_dir):
            recursive_mkdir(client_config.image_dir)
        if not path.isdir(database_directory):
            recursive_mkdir(database_directory)

        conn = sqlite3.connect(client_config.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if cursor.fetchall().__str__().find('file') == -1:
            conn.execute('''create table file(
                            id integer primary key autoincrement not null,
                            file_name text unique not null,
                            file_path text not null ,
                            file_type text not null ,
                            hash_value text not null ,
                            transferred integer not null default 0
                        );''')
            conn.commit()
        conn.close()

    def record_video(self, capture_duration=10):
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        vid_path = client_config.video_dir + 'vid' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.mp4'
        out = cv2.VideoWriter(vid_path, fourcc, 20.0, (640, 480))

        start_time1 = time.time()
        while int(time.time() - start_time1) < capture_duration:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 90)
                out.write(frame)
                img_path = client_config.image_dir + 'img' + datetime.datetime.now().strftime(
                    "%Y-%m-%d_%H-%M-%S") + '.jpg'
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
        aud_path = client_config.audio_dir + 'aud' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.wav'
        wf = wave.open(aud_path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(form))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        self.files.append([aud_path, "audio"])
        self.save_to_db()

    def save_to_db(self):
        start_time = time.time()
        # wait for video to save
        while int(time.time() - start_time) < 5:
            pass
        conn = sqlite3.connect(client_config.database_path)
        for file in self.files:
            try:
                conn.execute("insert into file (file_name, file_path, file_type, hash_value) values (?,?,?,?)",
                             (path.basename(file[0]), file[0], file[1], md5(open(file[0], 'rb').read()).hexdigest()))
                conn.commit()
            except sqlite3.IntegrityError:
                continue
        self.files = []
        conn.close()


if __name__ == "__main__":
    capture = Capture()
    capture.record_audio()
    capture.record_video()
