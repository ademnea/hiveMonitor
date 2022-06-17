import os
import platform
current_system = platform.system().lower()
if current_system == 'linux':
    file = open('/etc/issue', 'r')
    curr_system = file.read().lower()
    if curr_system.find('rasp') > -1:
        current_system = 'raspbian'

# user credentials
username = "mayweather"
password = "mayw"

# directories/paths used for image, video, audio, database
base_dir = os.getcwd()+"/client_info/"
video_dir = base_dir+"multimedia/videos/"
audio_dir = base_dir+"multimedia/audios/"
image_dir = base_dir+"multimedia/images/"
database_path = base_dir+"database.sqlite"

# server details
server_address = "0.0.0.0"

# transfer flags for database table => file, column transferred
TRANS_LIMIT = 5
