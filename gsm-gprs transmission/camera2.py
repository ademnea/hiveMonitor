from picamera import PiCamera
import time
camera = PiCamera()
camera.vflip=True
time.sleep(2)
i=0
for i in range(5):
    camera.capture("img"+str(i)+".jpg")
    file_name = "img"+str(i)+".h264"
    print("Start recording...")
    camera.start_recording(file_name)
    camera.wait_recording(5)
    camera.stop_recording()
    print("Done.")
    time.sleep(5)
print("Camera is Done.")