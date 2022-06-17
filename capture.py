from os import path, mkdir
from hashlib import md5
import sqlite3
import time
import client_config

if client_config.current_system == 'raspbian':
    import raspbian_capture as device_capture
else:
    import linux_capture as device_capture


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
    capture.snap(5)
    capture.record_audio()
    capture.record_video()
