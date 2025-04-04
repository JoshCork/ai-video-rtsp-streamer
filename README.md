THESE ARE OLD INSTRUCTIONS THAT CAN BE IGNORED FOR NOW

# AI Video RTSP Streamer

## Project Overview
This project provides a tool for streaming video content over RTSP (Real Time Streaming Protocol). It's designed to stream video files through a MediaMTX server, which can then be accessed by RTSP clients like VLC media player.

## Current Issue
We're experiencing an issue with the video stream terminating prematurely:

1. **Initial Setup Works:**
   - MediaMTX server starts successfully on port 8554
   - FFmpeg stream connects to the server
   - Video begins streaming

2. **Stream Termination:**
   - Stream runs for exactly one loop of the video (8.60 seconds)
   - FFmpeg reports: `time=00:00:08.56 bitrate=N/A speed=1.06x`
   - Server logs: `[RTSP] [session 1d2ee4f1] destroyed: torn down by 127.0.0.1:50966`
   - Stream stops despite `-stream_loop -1` parameter

3. **Attempted Solutions:**
   - Updated MediaMTX configuration
   - Modified FFmpeg streaming parameters
   - Added TCP transport mode
   - Implemented video looping

## Technical Details
- Server: MediaMTX v1.5.1
- Protocol: RTSP over TCP
- Video: 1080p, 25fps, 5000kb/s
- Source Duration: 8.60 seconds
- Stream URL: rtsp://192.168.86.65:8554/stream

## Setup Instructions
1. Start MediaMTX server:
   ```bash
   cd AI-Video-RTSP-STREAMER
   ./mediamtx
   ```

2. Start video stream:
   ```bash
   source venv/bin/activate
   video-streamer stream --video apple --fps 25
   ```

3. Access stream in VLC:
   - Media > Open Network Stream
   - URL: rtsp://192.168.86.65:8554/stream

## Next Steps
1. Investigate why the stream loop parameter isn't working
2. Check for MediaMTX session timeout settings
3. Consider implementing auto-reconnect in the Python code
4. Monitor server and client connection states

## Components
1. **MediaMTX Server**: A media streaming server that supports multiple protocols including RTSP
2. **Video Streamer**: A Python-based tool that uses FFmpeg to stream video content to the MediaMTX server
3. **Configuration**: Uses `mediamtx.yml` for server configuration

## Current Setup
- Server IP: 192.168.86.65
- RTSP Port: 8554
- Stream URL: rtsp://192.168.86.65:8554/stream
- Video Format: 1080p, 25fps, 5000kb/s bitrate

## Current Issues
We're experiencing several challenges:

1. **MediaMTX Server Stability**:
   - The server appears to be crashing or not starting properly
   - Logs show configuration issues with the protocols section
   - Current error: `ERR: json: cannot unmarshal object into Go struct field alias.protocols of type []string`

2. **Stream Connection**:
   - FFmpeg is unable to establish a connection to the RTSP server
   - The stream starts but terminates unexpectedly
   - VLC client cannot connect to the stream

## Troubleshooting Steps Taken
1. Modified MediaMTX configuration:
   - Simplified protocols to TCP only
   - Set explicit IP binding (0.0.0.0:8554)
   - Removed authentication requirements

2. Updated streaming parameters:
   - Matched source video frame rate (25fps)
   - Added TCP transport mode
   - Implemented video looping

## Usage
1. Start the MediaMTX server:
   ```bash
   cd AI-Video-RTSP-STREAMER
   ./mediamtx
   ```

2. In a separate terminal, start the video stream:
   ```bash
   source venv/bin/activate
   video-streamer stream --video apple --fps 25
   ```

3. Connect with VLC:
   - Open VLC
   - Media > Open Network Stream
   - Enter: rtsp://192.168.86.65:8554/stream

## Features

- Stream videos over RTSP protocol
- Download and manage video files
- Configure streaming parameters (resolution, framerate, bitrate)
- Inspect video metadata
- List available videos

## Requirements

- Python 3.8+
- Go 1.21+ (required for MediaMTX server)
- FFmpeg
- curl

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JoshCork/AI-Video-RTSP-STREAMER.git
cd AI-Video-RTSP-STREAMER
```

2. Install system dependencies:
```bash
# Install Go (if not already installed)
sudo apt install golang-go

# Install FFmpeg (if not already installed)
sudo apt install ffmpeg

# Install curl (if not already installed)
sudo apt install curl
```

3. Create and activate Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Stream a video
```bash
video-streamer stream --video apple --resolution 1080p --fps 25
```

### Download a new video
```bash
video-streamer download --url <URL> --name banana
```

### List available videos
```bash
video-streamer list
```

### Show video metadata
```bash
video-streamer info --video apple
```

## Configuration

Streaming parameters can be configured via command-line flags or defaults can be set in the config file.

Default parameters:
- Resolution: 1920x1080
- Framerate: 25 fps
- Bitrate: 5000 kb/s
- RTSP URL: rtsp://localhost:8554/stream

## License

MIT License
