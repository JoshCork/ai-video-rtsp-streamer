This will implement the "AI Video RTSP Streamer" user story you’ve outlined. Below, I’ll detail the folder structure and provide the code for each file, ensuring it meets the requirements for video management, streaming control, and integration with an AI processing NUC.

The system will:
- Use **MediaMTX** as the RTSP server (assumed to be running separately).
- Leverage **FFmpeg** for video processing and streaming.
- Provide a **Python CLI** for control, built with the `click` library.
- Include configuration management via a YAML file.
- Handle basic error cases and process management.

Let’s start with the folder structure and then provide the code for each file.

---

### Folder Structure

The project will be organized as follows:

```
ai-video-streamer/
├── videos/
│   # Directory to store video files (initially empty)
├── config.yaml
│   # Configuration file for default streaming parameters and RTSP settings
├── requirements.txt
│   # List of Python dependencies
├── README.md
│   # Instructions for setup and usage
└── src/
    ├── __init__.py
    │   # Empty file to mark src/ as a Python package
    ├── cli.py
    │   # Command-line interface implementation
    ├── video_manager.py
    │   # Functions for listing and downloading videos
    ├── streamer.py
    │   # Functions for starting and stopping streams
    └── utils.py
    │   # Utility functions (e.g., config loading, IP retrieval)
```

This structure separates concerns:
- `videos/` holds the video library.
- `config.yaml` stores defaults.
- `src/` contains the Python code, split into modules for clarity.

---

### Code for Each File

Below is the initial code for each file, designed to meet the user story requirements. You can copy this directly into Cursor and let the AI Assistant refine or expand it as needed.

#### **`config.yaml`**
This file defines default streaming parameters and RTSP settings.

```yaml
stream:
  fps: 25
  resolution: "1920x1080"
  bitrate: "5M"
  loop: true
rtsp:
  host: "localhost"
  port: 8554
  path: "stream"
```

- **Explanation**: 
  - `stream`: Default settings for FPS, resolution, bitrate, and looping.
  - `rtsp`: Settings for the RTSP server (MediaMTX). `host` is `localhost` for FFmpeg (since it runs on the same machine), but we’ll display the network IP to users.

---

#### **`requirements.txt`**
Lists the Python libraries needed for the project.

```
click
opencv-python
pyyaml
requests
```

- **Explanation**: 
  - `click`: For the CLI.
  - `opencv-python`: To extract video metadata (FPS, resolution).
  - `pyyaml`: To parse the config file.
  - `requests`: For downloading videos.

Note: FFmpeg must be installed separately on the system, and MediaMTX should be running.

---

#### **`README.md`**
Provides setup and usage instructions.

```markdown
# AI Video RTSP Streamer

A Python CLI tool to manage and stream videos via RTSP for AI processing.

## Prerequisites

- Python 3.x
- FFmpeg installed (e.g., `sudo apt install ffmpeg` on Ubuntu)
- MediaMTX running (download from https://github.com/bluenviron/mediamtx)
- Network access between the streaming NUC and AI processing NUC

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run MediaMTX**:
   - Start MediaMTX on the NUC (default port: 8554).
   - Ensure it’s accessible on the network (listens on 0.0.0.0:8554 by default).

3. **Prepare videos**:
   - Place videos in the `videos/` directory or use the `download` command.

## Usage

- **List available videos**:
  ```bash
  python src/cli.py list
  ```

- **Download a video**:
  ```bash
  python src/cli.py download --url https://example.com/video.mp4 --name test
  ```

- **Start streaming**:
  ```bash
  python src/cli.py stream --video apple --fps 15
  ```
  - Omit `--fps` to use the video’s original FPS or config default.

- **Stop streaming**:
  ```bash
  python src/cli.py stop
  ```

- **RTSP Endpoint**:
  - Access the stream at `rtsp://<nuc-ip>:8554/stream` from the AI processing NUC.

## Notes

- Ensure the `videos/` directory exists before running commands.
- Streaming parameters can be customized via CLI options or `config.yaml`.
```

- **Explanation**: Guides the user through setup and usage, mirroring the example flow in the user story.

---

#### **`src/__init__.py`**
An empty file to make `src/` a Python package.

```python
# This file is intentionally empty
```

---

#### **`src/cli.py`**
Implements the command-line interface using `click`.

```python
import click
from .video_manager import list_videos, download_video
from .streamer import start_stream, stop_stream
from .utils import load_config, get_ip

@click.group()
def cli():
    """AI Video RTSP Streamer CLI."""
    pass

@cli.command()
def list():
    """List available videos in the local library."""
    list_videos()

@cli.command()
@click.option('--url', required=True, help='URL of the video to download')
@click.option('--name', required=True, help='Name to save the video as')
def download(url, name):
    """Download a video from a URL."""
    download_video(url, name)

@cli.command()
@click.option('--video', required=True, help='Name of the video to stream (without .mp4)')
@click.option('--fps', type=float, help='Frame rate for streaming')
@click.option('--resolution', help='Resolution (e.g., 1280x720)')
@click.option('--bitrate', help='Bitrate (e.g., 2M)')
@click.option('--loop', is_flag=True, help='Loop the video continuously')
def stream(video, fps, resolution, bitrate, loop):
    """Start streaming a video via RTSP."""
    config = load_config()
    # Use CLI options if provided, otherwise fall back to config defaults
    fps = fps if fps is not None else config['stream']['fps']
    resolution = resolution if resolution is not None else config['stream']['resolution']
    bitrate = bitrate if bitrate is not None else config['stream']['bitrate']
    loop = loop if loop is not None else config['stream']['loop']
    
    # Stop any existing stream before starting a new one
    stop_stream()
    start_stream(video, fps, resolution, bitrate, loop)
    
    # Display the RTSP URL with the NUC's IP for external access
    ip = get_ip()
    rtsp_url = f"rtsp://{ip}:{config['rtsp']['port']}/{config['rtsp']['path']}"
    print(f"Stream started at {rtsp_url}")

@cli.command()
def stop():
    """Stop the current stream."""
    stop_stream()

if __name__ == '__main__':
    cli()
```

- **Explanation**: 
  - Defines four commands: `list`, `download`, `stream`, and `stop`.
  - The `stream` command uses CLI options or config defaults, stops any existing stream, starts a new one, and displays the RTSP URL with the NUC’s IP.

---

#### **`src/video_manager.py`**
Handles video listing and downloading.

```python
import os
import cv2
import requests

VIDEO_DIR = 'videos'

def get_video_info(video_path):
    """Extract video metadata using OpenCV."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return {"fps": fps, "resolution": (width, height)}

def list_videos():
    """List all videos in the videos/ directory with metadata."""
    if not os.path.exists(VIDEO_DIR):
        print("No videos directory found. Create 'videos/' and add some videos.")
        return
    for file in os.listdir(VIDEO_DIR):
        if file.endswith('.mp4'):
            path = os.path.join(VIDEO_DIR, file)
            info = get_video_info(path)
            if info:
                res = f"{info['resolution'][1]}p"
                fps = f"{info['fps']:.2f}fps"
                print(f"{file} ({res}, {fps})")

def download_video(url, name):
    """Download a video from a URL and save it to the videos/ directory."""
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)
    dest = os.path.join(VIDEO_DIR, name + '.mp4')
    if os.path.exists(dest):
        print(f"Video {name}.mp4 already exists.")
        return
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {name}.mp4")
    except requests.RequestException as e:
        print(f"Failed to download: {e}")
```

- **Explanation**: 
  - `get_video_info`: Uses OpenCV to extract FPS and resolution.
  - `list_videos`: Scans `videos/` and prints video names with metadata (e.g., "apple.mp4 (1080p, 25fps)").
  - `download_video`: Downloads a video using `requests`, saves it as `<name>.mp4`, and handles basic errors.

---

#### **`src/streamer.py`**
Manages starting and stopping FFmpeg streaming processes.

```python
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
    cmd += ['-c:v', 'libx264', '-an', '-f', 'rtsp', rtsp_url]  # Encode to H.264, no audio, RTSP output
    return cmd

def start_stream(video, fps, resolution, bitrate, loop):
    """Start streaming a video to the RTSP server."""
    config = load_config()
    video_path = os.path.join(VIDEO_DIR, video + '.mp4')
    if not os.path.exists(video_path):
        print(f"Video {video}.mp4 does not exist.")
        return
    rtsp_url = f"rtsp://{config['rtsp']['host']}:{config['rtsp']['port']}/{config['rtsp']['path']}"
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
```

- **Explanation**: 
  - `build_ffmpeg_command`: Creates an FFmpeg command with configurable parameters.
  - `start_stream`: Launches FFmpeg to stream to MediaMTX and saves the process ID.
  - `stop_stream`: Terminates the FFmpeg process using the saved PID.

---

#### **`src/utils.py`**
Contains utility functions.

```python
import yaml
import socket

def load_config():
    """Load the configuration from config.yaml."""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def get_ip():
    """Get the machine's network IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip
```

- **Explanation**: 
  - `load_config`: Reads `config.yaml`.
  - `get_ip`: Retrieves the NUC’s IP for displaying the RTSP URL.

---

### How This Meets the User Story

#### **Video Management**
- **List videos**: `list_videos()` scans `videos/` and shows names with metadata.
- **Download videos**: `download_video()` fetches videos from URLs and stores them in `videos/`.
- **Managed directory**: All videos are stored in `videos/`.

#### **Streaming Control**
- **Start/stop**: `stream` and `stop` commands control FFmpeg processes.
- **Parameters**: CLI options (`--fps`, `--resolution`, `--bitrate`, `--loop`) override config defaults.
- **Continuous streaming**: `-stream_loop -1` in FFmpeg enables looping.

#### **Integration**
- **RTSP endpoint**: Streams to `rtsp://<nuc-ip>:8554/stream`, accessible by the AI NUC.
- **Reliability**: MediaMTX ensures a stable connection; FFmpeg handles processing.
- **Multiple viewers**: MediaMTX supports concurrent clients connecting to the same stream.

#### **Technical Requirements**
- **MediaMTX**: Used as the RTSP server (assumed running).
- **FFmpeg**: Processes and streams videos.
- **Python CLI**: Built with `click`.
- **Config management**: `config.yaml` provides defaults.
- **Error handling**: Basic checks for file existence, download failures, and process management.
- **Process management**: PID file tracks the FFmpeg process.

---

### Next Steps in Cursor

You can paste this entire structure and code into Cursor and ask your AI Assistant to:
- Add detailed logging (e.g., using the `logging` module).
- Enhance error handling (e.g., validate resolution formats, handle FFmpeg crashes).
- Implement progress bars for downloads using `tqdm`.
- Add a command to check or start MediaMTX if desired.

This starter provides a functional base that the AI Assistant can build upon based on your further instructions! Let me know if you need adjustments before handing it off.