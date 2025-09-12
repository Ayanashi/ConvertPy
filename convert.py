## A script to convert MP4 video files to MP3 audio files using FFmpeg.
# require tqdm>=4.60.0
import os
import subprocess
import threading
import time
from pathlib import Path
import logging
import sys

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("conversion.log"), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class VideoToAudioConverter:
    def __init__(
        self,
        bitrate="192k",
        samplerate=44100,
        output_dir=None,
        delete_original=False,
        overwrite=False,
        output_format="mp3",
    ):
        self.bitrate = bitrate
        self.samplerate = samplerate
        self.output_dir = output_dir
        self.delete_original = delete_original
        self.overwrite = overwrite
        self.output_format = output_format.lower()
        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)

    def check_ffmpeg_installed(self):
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def get_video_duration(self, file_path):
        try:
            cmd = [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(file_path),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except Exception:
            return 0

    def convert_video_to_audio(self, input_file, progress_callback=None):
        if self.output_dir:
            output_path = Path(self.output_dir) / (
                Path(input_file).stem + f".{self.output_format}"
            )
        else:
            output_path = Path(input_file).with_suffix(f".{self.output_format}")

        if output_path.exists() and not self.overwrite:
            logger.warning(f"{output_path} exists, skipping.")
            return False

        duration = self.get_video_duration(input_file)

        cmd = [
            "ffmpeg",
            "-i",
            str(input_file),
            "-vn",
            "-acodec",
            "libmp3lame" if self.output_format == "mp3" else "pcm_s16le",
            "-ab",
            self.bitrate,
            "-ar",
            str(self.samplerate),
            "-y" if self.overwrite else "-n",
            "-loglevel",
            "error",
            str(output_path),
        ]

        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )

        if duration > 0 and progress_callback:
            t = threading.Thread(
                target=self.monitor_progress,
                args=(process, duration, progress_callback, input_file),
            )
            t.daemon = True
            t.start()

        stdout, stderr = process.communicate()
        if process.returncode == 0:
            logger.info(f"Converted: {input_file} -> {output_path}")
            if self.delete_original:
                os.remove(input_file)
            return True
        else:
            logger.error(f"Error converting {input_file}: {stderr}")
            return False

    def monitor_progress(self, process, duration, callback, filename):
        start = time.time()
        while process.poll() is None:
            elapsed = time.time() - start
            progress = min(100, (elapsed / duration) * 100)
            callback(filename, progress)
            time.sleep(0.5)
        callback(filename, 100)


# Wrapper for tests
def convert_to_audio(
    input_file, output_file, bitrate="192k", samplerate=44100, overwrite=False
):
    converter = VideoToAudioConverter(
        bitrate=bitrate, samplerate=samplerate, overwrite=overwrite
    )
    return converter.convert_video_to_audio(input_file)
