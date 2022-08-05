#!/bin/bash
apt update
pip install --upgrade pip setuptools wheel
pip install picamera
apt install libportaudio0 portaudio19-dev python3-pyaudio libportaudio2 libportaudiocpp0
pip install pyaudio
apt install -y gpac