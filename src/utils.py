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