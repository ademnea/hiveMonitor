import os
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
TRANS_INCOMPLETE = 0
TRANS_COMPLETE = 1
