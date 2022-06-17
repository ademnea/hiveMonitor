import os

# server configurations
address = "0.0.0.0"
port = 21

# base directory and users directory
base_dir = os.getcwd()+"/server_info/"
users_dir = base_dir+"users/"

# multimedia directories for each user => (individual user directory + multimedia directory)
user_video_dir = "/videos/"
user_audio_dir = "/audios/"
user_image_dir = "/images/"

# database path
database_path = base_dir+"database.sqlite"



