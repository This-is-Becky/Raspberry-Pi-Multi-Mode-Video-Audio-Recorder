# -*- coding: utf-8 -*-
"""
Created on Mon Sep  1 09:31:01 2023

@author: beckylin
"""

import os
import time
import shutil
import threading
import subprocess
from datetime import datetime, timedelta
import serial
import importlib

function = input("Enter Function Mode (1: Video+Audio, 2: Video Only, 3: Separate Audio/Video): ").strip()
#function =3  # Change to 2 or 3 mode as needed
module_name = f"mode{function}"
record_module = importlib.import_module(module_name)
record = record_module.record

# Serial setup
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1)

# Constants
DISTANCE_THRESHOLD = 75
RECORD_DURATION = 120  # seconds
STABILITY_TIME = 3     # seconds
FOLDER_PATH = "/home/pi/Documents/Image"

def get_sound_path():
    return os.path.join(FOLDER_PATH, datetime.today().strftime('%Y%m%d'))
#for wav.files
def create_folder_and_filename():
    path = get_sound_path()
    os.makedirs(path, exist_ok=True)
    filename = os.path.join(path, f"{datetime.today().strftime('%Y%m%d_%H%M%S%f')}.wav")
    return filename
#for mp4.files
def create_vid_file():
    path = get_sound_path()
    os.makedirs(path, exist_ok=True)
    filename = os.path.join(path, f"{datetime.today().strftime('%Y%m%d_%H%M%S%f')}.mp4")
    return filename

def delete_old_folders(base_path, days_old=10):
    now = datetime.now()
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        try:
            folder_date = datetime.strptime(folder, '%Y%m%d')
            if now - folder_date > timedelta(days=days_old):
                shutil.rmtree(folder_path)
                print(f"Deleted old folder: {folder_path}")
        except ValueError:
            continue

class RecorderThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        print("Recorder thread started.")
        recording = False
        process = None
        filename = None

        while not self._stop_event.is_set():
            try:
                data = ser.readline().decode('utf-8').strip()
                distance = int(data)
                print(distance)

                if distance <= DISTANCE_THRESHOLD and not recording:
                    # Stability check
                    stable = True
                    start = time.perf_counter()
                    while time.perf_counter() - start < STABILITY_TIME:
                        data = ser.readline().decode('utf-8').strip()
                        distance = int(data)
                        if distance > DISTANCE_THRESHOLD:
                            stable = False
                            break

                    if stable:
                        filename = create_vid_file()
                        
                        if function == 3:
                            audio_filename = create_folder_and_filename()
                            record(RECORD_DURATION, filename, audio_filename)
                        else:
                            record(RECORD_DURATION, filename)

                        recording = True
                        print("Video recording started.")

                        start = time.perf_counter()
                        while time.perf_counter() - start < RECORD_DURATION:
                            data = ser.readline().decode('utf-8').strip()
                            distance = int(data)
                            if distance > DISTANCE_THRESHOLD:
                                process.terminate()
                                recording = False
                                print("Video recording stopped early.")
                                break

                        if recording:
                            process.terminate()
                            recording = False
                            print("Video recording completed.")

                        # Wait until distance is back above threshold
                        while True:
                            data = ser.readline().decode('utf-8').strip()
                            distance = int(data)
                            if distance > DISTANCE_THRESHOLD:
                                break

            except ValueError:
                if data == "Out of range":
                    print("Received data: Out of range")
                    if recording:
                        print("Stopping video due to out of range...")
                        process.terminate()
                        recording = False
                else:
                    print("Invalid data received")

            time.sleep(0.05)


class CleanupThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        print("Cleanup thread started.")
        while not self._stop_event.is_set():
            try:
                delete_old_folders(FOLDER_PATH)
            except Exception as e:
                print(f"Cleanup error: {e}")
            time.sleep(0.1)

if __name__ == '__main__':
    try:
        recorder = RecorderThread()
        cleaner = CleanupThread()
        recorder.start()
        cleaner.start()

        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Stopping threads...")
        recorder.stop()
        cleaner.stop()
        recorder.join()
        cleaner.join()
        ser.close()
        print("Program terminated.")
