
#Record only video, withoud audio, for better file storage, or only motion detection
import subprocess

def record(RECORD_DURATION, filename):
    process = subprocess.Popen([
        'ffmpeg',
        '-f', 'v4l2', '-framerate', '30', '-video_size', '1280x720',
        '-i', '/dev/video0',
        '-vcodec', 'libx264', '-preset', 'ultrafast',
        '-crf', '23',
        '-t', str(RECORD_DURATION),
        filename
    ])
    return process
