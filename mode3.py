
#Save wav and mp4 file in seperat file, for better futher analysis
import subprocess

def record(RECORD_DURATION, video_filename, audio_filename):
    video_process = subprocess.Popen([
        'ffmpeg',
        '-f', 'v4l2', '-framerate', '30', '-video_size', '1280x720',
        '-i', '/dev/video0',
        '-vcodec', 'libx264', '-preset', 'ultrafast', '-crf', '23',
        '-t', str(RECORD_DURATION),
        video_filename
    ])
    
    #Using arecord for audio raw data, advantage for futher analysis
    audio_process = subprocess.Popen([
        'arecord',
        '-D', 'plughw:3,0',
        '--format=FLOAT_LE',
        '--rate=44100',
        '-c2',
        '-d', str(RECORD_DURATION),
        audio_filename
    ])

    return video_process, audio_process
