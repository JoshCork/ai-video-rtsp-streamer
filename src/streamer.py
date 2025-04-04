import os
import subprocess
import signal
from .utils import load_config

VIDEO_DIR = 'videos'
PID_FILE = 'stream.pid'

def build_ffmpeg_command(video_path, fps, resolution, bitrate, loop, rtsp_url):
    """Construct the FFmpeg command for streaming."""
    cmd = ['ffmpeg']
    if loop:
        cmd += ['-stream_loop', '-1']  # Loop the video indefinitely
    cmd += ['-re', '-i', video_path]  # Read at real-time rate
    if fps:
        cmd += ['-r', str(fps)]  # Set output frame rate
    if resolution:
        cmd += ['-s', resolution]  # Set resolution
    if bitrate:
        cmd += ['-b:v', bitrate]  # Set bitrate
    # Added more compatible encoding parameters for VLC
    cmd += [
        '-c:v', 'libx264',
        '-preset', 'veryfast',  # Faster encoding
        '-tune', 'zerolatency',  # Reduce latency
        '-an',  # No audio
        '-f', 'rtsp',
        '-rtsp_transport', 'tcp',
        rtsp_url
    ]
    return cmd

def start_stream(video, fps, resolution, bitrate, loop):
    """Start streaming a video to the RTSP server."""
    config = load_config()
    video_path = os.path.join(VIDEO_DIR, video + '.mp4')
    if not os.path.exists(video_path):
        print(f"Video {video}.mp4 does not exist.")
        return
    # Using stream0 as the path for better compatibility
    rtsp_url = f"rtsp://{config['rtsp']['host']}:{config['rtsp']['port']}/stream0"
    cmd = build_ffmpeg_command(video_path, fps, resolution, bitrate, loop, rtsp_url)
    proc = subprocess.Popen(cmd)
    with open(PID_FILE, 'w') as f:
        f.write(str(proc.pid))

def stop_stream():
    """Stop the current streaming process."""
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read())
        os.kill(pid, signal.SIGTERM)
        os.remove(PID_FILE)
        print("Stream stopped.")
    except FileNotFoundError:
        print("No stream is running.")
    except ProcessLookupError:
        print("Stream process not found.")
        os.remove(PID_FILE) 