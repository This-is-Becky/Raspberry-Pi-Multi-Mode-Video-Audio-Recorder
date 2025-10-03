# Raspberry-Pi-Multi-Mode-Video-Audio-Recorder
This Python-based recording system for Raspberry Pi captures video and/or audio triggered by the distance sensor. It supports three flexible recording modes tailored for different use cases.

## For Distance.ino file
Connect VL53L0X sensor to ESP32 and upload the script on ESP32 

## For Various_record.py file
- Distance-triggered recording when the object is within a threshold using serial sensor input.
- Dynamically loads the appropriate recording module (mode1, mode2, or mode3) based on user input or configuration.
- Automatic folder creation and cleanup for storage management

## For mode1/ mode2/ mode3.py files
- Mode 1: Record video and audio together into a single .mp4 file. **Best for general-purpose recording and playback.**
- Mode 2: Record only video (no audio) for lightweight storage. **Ideal for motion detection, storage efficiency, or silent environments.**
- Mode 3: Record video and audio separately into .mp4 and .wav files. **Best for post-processing, machine learning, or audio analysis.**

## Hardware Requirements

- Raspberry Pi
- USB camera or any Webcam
- Microphone (USB or ALSA-compatible)
- Distance sensor connected via serial(VL53L0X)

## Software Setup

- Install Python 3 and FFmpeg:
```
sudo apt update
```
```
sudo apt install python3 ffmpeg
```
```
pip3 install pyserial
```

## Step by Step
- Place the **Various_record**, **mode1**, **mode2**, **mode3** pythons file in the project folder
(/home/pi/Documents)
- Place the **Execute_code** shell file in the same path as above
- Make it executable
```
chmod +x Execute_code.sh
```
- Run the sh file
```
./Execute_code.sh
```

- Change the definition as the avaliable devices detected after the sh file runs

<img width="1313" height="174" alt="image" src="https://github.com/user-attachments/assets/0046f8f8-783c-47bd-98b7-528fb6abc513" />


-  For Distance sensor
```
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1)
```

- For camera device
**`/dev/video0'`** define in mode1 to 3.py files
```
    process = subprocess.Popen([
    'ffmpeg', '-f', 'v4l2', '-framerate', '30', '-video_size', '1280x720',
    '-i', '/dev/video0', '-f', 'alsa', '-i', 'plughw:2,0',
    '-vcodec', 'libx264', '-preset', 'ultrafast', 
    '-crf', '23', '-t', str(RECORD_DURATION), filename
    ])
```

- For audio device
**`plughw:2,0`** define in mode1 to 3.py files
```
    process = subprocess.Popen([
    'ffmpeg', '-f', 'v4l2', '-framerate', '30', '-video_size', '1280x720',
    '-i', '/dev/video0', '-f', 'alsa', '-i', 'plughw:2,0',
    '-vcodec', 'libx264', '-preset', 'ultrafast', 
    '-crf', '23', '-t', str(RECORD_DURATION), filename
    ])
```
