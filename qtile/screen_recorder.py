"""Screen recording toggle for the bar widget.

IMPORTANT - everything here runs INSIDE qtile's event loop, synchronously,
because the widget's mouse_callback is a lazy.function. Two rules follow:

  1. Never invoke a Wayland client (wlr-randr, grim, wl-copy...) from here.
     Such a client connects back to qtile and blocks on a roundtrip that qtile
     cannot service while it is blocked waiting for that client to exit. That
     is a hard deadlock: the whole desktop freezes with no way out. This file
     did exactly that on 2026-08-29 via wlr-randr and locked the session.

  2. Never wait on a subprocess. No .wait(), no .communicate(), no
     check_output() on anything slow. Fire and poll.

Output geometry therefore comes from qtile's own in-process screen info, and
stopping the recorder signals the process without waiting for it to die - the
1-second widget poll reports when it is actually gone.
"""

import shutil
import signal
import subprocess
from datetime import datetime
from pathlib import Path

from libqtile import qtile
from libqtile.log_utils import logger

from backend import IS_WAYLAND

recording_process = None
output_file_path = None
_stopping = False


def _default_audio_source():
    """First non-monitor PulseAudio source, else the server default.

    pactl is not a Wayland client, so this cannot deadlock, but it is still a
    blocking call in the event loop - hence the short timeout.
    """
    try:
        out = subprocess.check_output(
            ["pactl", "list", "sources", "short"], text=True, timeout=2
        )
        for line in out.splitlines():
            parts = line.split("\t") if "\t" in line else line.split()
            if len(parts) > 1 and "monitor" not in parts[1]:
                return parts[1]
    except Exception as e:
        logger.warning("screen_recorder: could not detect audio source: %s", e)
    return "@DEFAULT_SOURCE@"


def _active_output():
    """Connector name of the focused screen, straight from qtile.

    In-process: no subprocess, no Wayland client, no deadlock. This replaced a
    `wlr-randr` call that froze the session.
    """
    try:
        return qtile.current_screen.info().get("port")
    except Exception as e:
        logger.warning("screen_recorder: could not determine output: %s", e)
        return None


def _x11_cmd(out_path, audio_source):
    return [
        "ffmpeg", "-y",
        "-f", "pulse", "-i", audio_source,
        "-f", "x11grab",
        "-framerate", "30",
        "-video_size", "1920x1080",
        "-i", ":0.0",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+frag_keyframe+empty_moov+faststart",
        str(out_path),
    ]


def _wayland_cmd(out_path, audio_source):
    cmd = ["wf-recorder", "-f", str(out_path), "-a", audio_source]
    output = _active_output()
    if output:
        cmd += ["-o", output]
    return cmd


def start_screen_recording():
    global recording_process, output_file_path, _stopping

    if recording_process and recording_process.poll() is None:
        logger.info("screen_recorder: already recording")
        return False

    videos_dir = Path.home() / "Videos"
    videos_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    output_file_path = videos_dir / f"record-{timestamp}.mp4"

    audio_source = _default_audio_source()
    cmd = (
        _wayland_cmd(output_file_path, audio_source)
        if IS_WAYLAND
        else _x11_cmd(output_file_path, audio_source)
    )

    if shutil.which(cmd[0]) is None:
        logger.error("screen_recorder: %s not found in PATH", cmd[0])
        return False

    try:
        # DEVNULL, not PIPE: nobody drains these pipes, so a chatty encoder
        # would fill the 64K buffer and block forever mid-recording.
        recording_process = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        _stopping = False
        logger.info("screen_recorder: started %s -> %s", cmd[0], output_file_path)
        return True
    except Exception as e:
        logger.exception("screen_recorder: failed to start: %s", e)
        recording_process = None
        return False


def stop_screen_recording():
    """Signal the recorder and return immediately.

    No .wait() - a blocking wait here freezes the entire compositor. The widget
    poll below notices when the process is actually gone and finalises.
    """
    global recording_process, _stopping

    if not (recording_process and recording_process.poll() is None):
        recording_process = None
        return False

    try:
        # SIGINT lets both ffmpeg and wf-recorder finalise the container.
        recording_process.send_signal(signal.SIGINT)
        _stopping = True
        logger.info("screen_recorder: stop signalled (pid %s)", recording_process.pid)
    except Exception as e:
        logger.exception("screen_recorder: error stopping: %s", e)
    return True


def get_recording_status_text():
    """Polled once a second by the widget; also reaps a finished process."""
    global recording_process, _stopping

    if recording_process is None:
        return "⚪"

    if recording_process.poll() is None:
        return "◼" if _stopping else "🔴"   # ◼ = finalising

    if _stopping:
        logger.info("screen_recorder: saved %s", output_file_path)
    recording_process = None
    _stopping = False
    return "⚪"


def toggle_recording():
    if recording_process and recording_process.poll() is None:
        stop_screen_recording()
    else:
        start_screen_recording()
    return get_recording_status_text()
