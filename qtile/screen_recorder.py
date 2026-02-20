import subprocess
import signal
from datetime import datetime
from pathlib import Path

recording_process = None
output_file_path = None


def start_screen_recording():
    global recording_process, output_file_path
    if recording_process and recording_process.poll() is None:
        print("Recording is already in progress.")
        return False

    timestamp = datetime.now().strftime(
        "%Y-%m-%d-%H-%M-%S"
    )  # Added seconds for uniqueness
    # Ensure Videos directory exists
    videos_dir = Path.home() / "Videos"
    videos_dir.mkdir(parents=True, exist_ok=True)
    output_file_path = videos_dir / f"record-{timestamp}.mp4"

    # Check for available audio source, this might need adjustment based on your system
    # You can find your source with `pactl list sources short`
    # Example: alsa_input.pci-0000_00_1f.3.analog-stereo
    # If you're unsure, you might need to make this configurable or detect it.
    # For now, using the one provided in the original script.
    audio_source = "alsa_input.pci-0000_00_1f.3.analog-stereo"

    cmd = [
        "ffmpeg",
        "-y",  # Overwrite output file if it exists
        "-f",
        "pulse",
        "-i",
        audio_source,
        "-f",
        "x11grab",
        "-framerate",
        "30",
        "-video_size",
        "1920x1080",  # Consider making this dynamic or configurable
        "-i",
        ":0.0",  # Assumes display is :0.0
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",  # Good for low CPU usage, but larger files
        "-crf",
        "23",  # Constant Rate Factor (lower is better quality, 18-28 is a good range)
        "-pix_fmt",
        "yuv420p",  # Common pixel format for compatibility
        "-c:a",
        "aac",
        "-b:a",
        "128k",  # Audio bitrate
        "-movflags",
        "+frag_keyframe+empty_moov+faststart",  # Faststart is good for web video
        str(output_file_path),
    ]

    try:
        print(f"Starting recording, output to: {output_file_path}")
        # Start process without shell=True for security and better process management
        recording_process = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(f"Recording started with PID: {recording_process.pid}")
        return True
    except FileNotFoundError:
        print(
            "ffmpeg command not found. Please ensure ffmpeg is installed and in your PATH."
        )
        recording_process = None
        return False
    except Exception as e:
        print(f"Failed to start recording: {e}")
        recording_process = None
        return False


def stop_screen_recording():
    global recording_process
    if (
        recording_process and recording_process.poll() is None
    ):  # Check if process exists and is running
        print(f"Stopping recording (PID: {recording_process.pid})...")
        try:
            # FFmpeg can be stopped gracefully by sending 'q' to its stdin
            # Or by sending SIGINT (Ctrl+C)
            recording_process.send_signal(signal.SIGINT)
            recording_process.wait(timeout=10)  # Wait for ffmpeg to finalize the file
            print(f"Recording stopped. Output saved to: {output_file_path}")
        except subprocess.TimeoutExpired:
            print("FFmpeg did not stop in time, killing process.")
            recording_process.kill()
            recording_process.wait()
            print("Recording process killed.")
        except Exception as e:
            print(f"Error stopping recording: {e}")
            # Fallback to kill if other methods fail
            if recording_process and recording_process.poll() is None:
                recording_process.kill()
                recording_process.wait()
            print("Recording process forcefully killed due to error during stop.")
        finally:
            recording_process = None
        return True
    else:
        print("No recording in progress to stop.")
        # Ensure process is cleared if it's already terminated
        if recording_process and recording_process.poll() is not None:
            recording_process = None
        return False


def get_recording_status_text():
    global recording_process
    if recording_process and recording_process.poll() is None:
        return "🔴"
    return "⚪"


def toggle_recording():
    # This function will be called by the Qtile widget's button press
    global recording_process
    if recording_process and recording_process.poll() is None:
        stop_screen_recording()
    else:
        start_screen_recording()
    return get_recording_status_text()


# For testing directly
if __name__ == "__main__":
    import time

    print(toggle_recording())  # Start
    time.sleep(5)
    print(toggle_recording())  # Stop
    time.sleep(2)
    print(toggle_recording())  # Start again
    time.sleep(5)
    print(toggle_recording())  # Stop again
    print("Test complete.")
