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
### Step 1
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
### Step 2
Build the project by running the commands
```sh
python build.py 
cd ..
```
This will build a version that is compatible with your raspberry Pi
### Step 3


