import config
import time
import uuid
import pyaudio
import wave
from subprocess import call

# paths
audio_dir = config.base_dir+"/multimedia/audios/"
database_path = config.base_dir+"/multimedia/database.sqlite"


class Capture:
    def __init__(self):
        self.files = []

    def change_format(self, file_path):
        new_file_path = file_path
        if file_path.endswith(".h264"):
            new_file_path = file_path[:-5]+".mp4"
            call("MP4Box -fps 30 -add "+file_path+" "+new_file_path, shell=True)
            call("rm "+file_path, shell=True)
        return new_file_path

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
        self.files.append([self.change_format(aud_path), "audio"])
        self.save_to_db()

    def save_to_db(self):
        pass
