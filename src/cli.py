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
    rtsp_url = f"rtsp://{ip}:{config['rtsp']['port']}/stream0"
    print(f"Stream started at {rtsp_url}")

@cli.command()
def stop():
    """Stop the current stream."""
    stop_stream()

if __name__ == '__main__':
    cli() 