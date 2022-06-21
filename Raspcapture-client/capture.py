from os import path, mkdir
from hashlib import md5
import sqlite3
import time
<<<<<<< HEAD
import config2

if config2.current_system == 'raspbian':
    import raspbian_capture as device_capture
else:
    import linux_capture as device_capture
=======
import config
import device_capture

# paths
video_dir = config.base_dir+"multimedia/videos/"
audio_dir = config.base_dir+"multimedia/audios/"
image_dir = config.base_dir+"multimedia/images/"
database_path = config.base_dir+"database.sqlite"
>>>>>>> 0c2cbd41787eb4fd9e8af69eac779e1fb694acff


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


class Capture(device_capture.Capture):
    def __init__(self):
        super().__init__()
<<<<<<< HEAD
        last_slash = config2.database_path.rindex('/')
        database_directory = config2.database_path[0:last_slash]

        # check if directories exist and if not create them
        if not path.isdir(config2.video_dir):
            recursive_mkdir(config2.video_dir)
        if not path.isdir(config2.audio_dir):
            recursive_mkdir(config2.audio_dir)
        if not path.isdir(config2.image_dir):
            recursive_mkdir(config2.image_dir)
        if not path.isdir(database_directory):
            recursive_mkdir(database_directory)

        conn = sqlite3.connect(config2.database_path)
=======
        last_slash = database_path.rindex('/')
        database_directory = database_path[0:last_slash]

        # check if directories exist and if not create them
        if not path.isdir(video_dir):
            recursive_mkdir(video_dir)
        if not path.isdir(audio_dir):
            recursive_mkdir(audio_dir)
        if not path.isdir(image_dir):
            recursive_mkdir(image_dir)
        if not path.isdir(database_directory):
            recursive_mkdir(database_directory)

        conn = sqlite3.connect(database_path)
>>>>>>> 0c2cbd41787eb4fd9e8af69eac779e1fb694acff
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

    def save_to_db(self):
        start_time = time.time()
        # wait for video to save
        while int(time.time() - start_time) < 5:
            pass
<<<<<<< HEAD
        conn = sqlite3.connect(config2.database_path)
=======
        conn = sqlite3.connect(database_path)
>>>>>>> 0c2cbd41787eb4fd9e8af69eac779e1fb694acff
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
    capture.snap(5)
    capture.record_audio()
    capture.record_video()
