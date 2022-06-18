Quick links
===========

-   [Home](https://github.com/timothy-mayweather/Raspcapture/Raspcapture-server)

About
=====
The Raspcapture-server module is built upon [pyftpdlib](https://pypi.org/project/pyftpdlib/), a very fast and reliable python server. It allows multiple user connections at a time, receives and saves their files each in their individual folder. Server configurations are set in the config.py file as follows:
- address of the server (default => "0.0.0.0")
- port on which it listens (default => 21)
- base directory (base_dir), the directory where server information will be stored (default => root_directory+"/server_info")
- users directory (users_dir), the directory where each user's folder will be stored by the server when they sign up (default => base_dir+"users/")
- the directories for each multimedia file received for each user. These directories will be created within individual user directories
    - video directory, user_video_dir (default = "/videos/")
    - audio directory, user_audio_dir (default = "/audios/")
    - image directory, user_image_dir (default = "/images/")
- database path, database_path (default = base_dir+"database.sqlite") 

The install.sh file contains packages to be installed for linux users

Features
========

- Extremely **lightweight**, **fast** and **scalable** 
- Uses sqlite database to store information about users and their files

Quick start
===========

In linux, open terminal in current directory & type 

```
sudo ./install.sh
python server.py
```