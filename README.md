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

