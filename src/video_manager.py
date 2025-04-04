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