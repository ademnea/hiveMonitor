# Raspcapture client
This is the cllient application. It runs on the raspberry pi (details are below). It performs the capturing of the images, recording of both 
audio and video, saving them and sending them to the remote server.

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
git clone https://github.com/ademnea/Raspcapture.git
```
When it runs successfully you will have the Raspcapture-client on the Pi
After that ensure that you go to the Raspcapture folder 
Run the command below
```sh
cd  Raspcapture
```
### Step 2: Building the project
Build the project by running the commands
```sh
python build.py 
cd ..
cd Raspcapture
```
This will build a version that is compatible with your raspberry Pi
### Step 3: Installing dependencies
```sh
sudo ./install.sh
```
### Step 4: Configuring the client
```sh
python setup.py
```
### Step 5: Running
There are two scripts 
- 1. capture.py - Captures the images, records both audio and video, saves them their information to a database
- 2. client.py - Sends the saved media files with the help of a database to the remote server.

#### Capturing
Ensure that the camera is enable otherwise the capture will not be successful
You can run the command below to see the configurations for your raspberry Pi
```sh
sudo raspi-config
```
This is done by running the command below
```sh
python capture.py
```
#### Sending
This is effected by the command 
```sh
python client.py
```
#### Final remarks
To automate the process of capturing and sending of the files cron jobs have to be set up to
run both scripts

