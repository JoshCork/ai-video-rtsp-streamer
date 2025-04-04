THESE ARE OLD INSTRUCTIONS THAT CAN BE IGNORED FOR NOW

# AI Video RTSP Streamer

A Python-based tool for streaming videos via RTSP, designed for AI video processing applications. This guide assumes you're new to Ubuntu Linux and will walk you through each step in detail.

## Features

- Download and manage video files
- Stream videos via RTSP with configurable parameters
- Support for frame rate, resolution, and bitrate control
- Video looping capability
- Simple command-line interface

## Prerequisites

Before you begin, you'll need:
- Ubuntu Linux (tested on Ubuntu 22.04 LTS)
- Python 3.7 or newer
- FFmpeg (for video processing)
- MediaMTX (RTSP server)

## Installation Guide

### 1. Open a Terminal
- Press `Ctrl + Alt + T` to open a terminal window
- Or click the "Activities" button in the top-left corner, type "terminal", and click on the Terminal icon

### 2. Install Required System Packages
First, update your system's package list and install necessary tools:
```bash
# Update package list
sudo apt-get update

# Install Git (if not already installed)
sudo apt-get install git

# Install Python3 and pip (Python package manager)
sudo apt-get install python3 python3-pip python3-venv
```

### 3. Set Up the Project
```bash
# Create a directory for your projects (if you don't have one)
mkdir -p ~/Source
cd ~/Source

# Clone this repository
git clone https://github.com/yourusername/ai-video-rtsp-streamer.git
cd ai-video-rtsp-streamer
```

### 4. Create and Activate a Python Virtual Environment
A virtual environment keeps project dependencies isolated:
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```
Note: You'll need to activate the virtual environment every time you open a new terminal window:
```bash
cd ~/Source/ai-video-rtsp-streamer
source venv/bin/activate
```

### 5. Install Python Dependencies
```bash
# Install required Python packages
pip install -r requirements.txt
```

### 6. Install FFmpeg
FFmpeg is required for video processing:
```bash
sudo apt-get install ffmpeg
```

### 7. Install MediaMTX
MediaMTX is the RTSP server that handles video streaming:
```bash
sudo apt-get install mediamtx
```

## Configuration

The default configuration is stored in `config.yaml`. You can modify these settings to match your needs:

```yaml
stream:
  fps: 25          # Frames per second
  resolution: "1920x1080"  # Video resolution
  bitrate: "5M"    # Video quality (5 megabits per second)
  loop: true       # Whether to loop the video
rtsp:
  host: "localhost"  # Server address (use your machine's IP for remote access)
  port: 8554        # RTSP port
  path: "stream"    # Stream path
```

## Usage Guide

### Starting the MediaMTX Server
Before streaming, you need to start the MediaMTX server:
```bash
# Start MediaMTX in the background
mediamtx &
```

### Managing Videos

1. List available videos:
```bash
# Make sure you're in the project directory and virtual environment is activated
cd ~/Source/ai-video-rtsp-streamer
source venv/bin/activate
python -m src.cli list
```

2. Download a video:
```bash
python -m src.cli download --url "https://example.com/video.mp4" --name "my_video"
```

### Streaming Videos

The streaming command supports several options to customize the stream:

```bash
python -m src.cli stream --video "my_video" [options]
```

Available options:
- `--video`: (Required) Name of the video to stream (without .mp4 extension)
- `--fps`: (Optional) Set custom frame rate (e.g., `--fps 15` for 15 FPS)
- `--resolution`: (Optional) Set custom resolution (e.g., `--resolution "1280x720"`)
- `--bitrate`: (Optional) Set custom bitrate (e.g., `--bitrate "2M"` for 2 Mbps)
- `--loop`: (Optional) Enable video looping (no value needed, just add the flag)

Examples:
```bash
# Basic streaming with default settings
python -m src.cli stream --video "pexels_apple_single"

# Stream at 15 FPS with looping
python -m src.cli stream --video "pexels_apple_single" --fps 15 --loop

# Stream at 720p resolution with 2 Mbps bitrate
python -m src.cli stream --video "pexels_apple_single" --resolution "1280x720" --bitrate "2M"

# Combine multiple options
python -m src.cli stream --video "pexels_apple_single" --fps 15 --resolution "1280x720" --bitrate "2M" --loop
```

### Stopping the Stream

To properly stop the stream, you need to do two things:

1. Stop the Python stream (in a new terminal window):
```bash
# Make sure you're in the project directory and virtual environment is activated
cd ~/Source/ai-video-rtsp-streamer
source venv/bin/activate
python -m src.cli stop
```

2. Stop the MediaMTX server:
```bash
pkill mediamtx
```

If you want to restart everything fresh:
```bash
# 1. Stop everything
source venv/bin/activate
python -m src.cli stop
pkill mediamtx

# 2. Start MediaMTX
mediamtx &

# 3. Start your stream
python -m src.cli stream --video "pexels_apple_single" --loop
```

Note: Simply pressing Ctrl+C in the terminal where the stream is running will not completely stop the stream. You need to follow the steps above to properly stop both the Python stream and the MediaMTX server.

### Connecting to the Stream
You can connect to the stream using VLC Media Player:
1. Open VLC
2. Go to Media → Open Network Stream
3. Enter the RTSP URL: `rtsp://your-ip-address:8554/stream`
   - Replace `your-ip-address` with your computer's IP address
   - You can find your IP address by running `ip addr show` in the terminal

## Troubleshooting

### Common Issues

1. "ModuleNotFoundError: No module named 'cv2'"
   - Make sure you've activated the virtual environment: `source venv/bin/activate`
   - Verify the package is installed: `pip list | grep opencv-python`

2. "Command not found: mediamtx"
   - Make sure MediaMTX is installed: `sudo apt-get install mediamtx`

3. Can't connect to the stream
   - Check if MediaMTX is running: `ps aux | grep mediamtx`
   - Verify your firewall settings allow traffic on port 8554
   - Make sure you're using the correct IP address

## Project Structure

- `src/`: Contains all Python source code
  - `cli.py`: Command-line interface
  - `streamer.py`: Video streaming functionality
  - `video_manager.py`: Video management utilities
  - `utils.py`: Helper functions
- `videos/`: Directory where downloaded videos are stored
- `config.yaml`: Configuration file
- `requirements.txt`: List of Python package dependencies

## License

MIT License
