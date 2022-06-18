#!/bin/bash
apt update
apt install python3
apt install pip
apt install ffmpeg libsm6 libxext6  -y
apt install portaudio19-dev
pip install opencv_camera
pip install pyAudio
