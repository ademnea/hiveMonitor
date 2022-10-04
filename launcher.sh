#!/bin/sh
#launcher.sh
#navigate to home directory, then to directory that has files
#then excecute python scripts for capturing and sending data

cd /
cd home/pi/capture
sudo python audio_capture.py
sudo python video_capture.py
sudo python image_capture.py
sudo python send_to_server.py

cd /



#make this script executable
#chmod 755 launcher.sh


#make logs directory
#mkdir logs


#Add to your crontab

#sudo crontab -e
# @reboot sh /home/pi/adm/launcher.sh >/home/pi/logs/cronlog 2>&1

