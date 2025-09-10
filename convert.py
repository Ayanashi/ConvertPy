## A script to convert MP4 video files to MP3 audio files using FFmpeg.
# require tqdm>=4.60.0
import os
import glob
import subprocess
import argparse
from pathlib import Path
from tqdm import tqdm
import logging
import sys
import threading
import time
import re

# Configure logging
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

    def get_file_size(self, file_path):
        """Get file size in MB"""
        return os.path.getsize(file_path) / (1024 * 1024)

    def check_ffmpeg_installed(self):
        """Check if ffmpeg is installed"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def get_video_duration(self, file_path):
        """Get video duration using ffprobe"""
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
        except (subprocess.CalledProcessError, ValueError):
            logger.warning(f"Could not get duration for {file_path}")
            return 0

    def convert_video_to_audio(self, input_file, progress_callback=None):
        """Convert a single video file to audio"""
        try:
            # Prepare output path
            if self.output_dir:
                output_filename = Path(input_file).stem + f".{self.output_format}"
                output_path = Path(self.output_dir) / output_filename
            else:
                output_path = Path(input_file).with_suffix(f".{self.output_format}")

            # Check if output file already exists
            if output_path.exists() and not self.overwrite:
                logger.warning(
                    f"File {output_path} already exists. Use --overwrite to overwrite."
                )
                return False

            # Get video duration for progress tracking
            duration = self.get_video_duration(input_file)

            # Prepare ffmpeg command
            cmd = [
                "ffmpeg",
                "-i",
                str(input_file),
                "-vn",  # No video
                "-acodec",
                "libmp3lame" if self.output_format == "mp3" else "pcm_s16le",
                "-ab",
                self.bitrate,
                "-ar",
                str(self.samplerate),
                "-y" if self.overwrite else "-n",
                "-loglevel",
                "error",  # Only errors
                str(output_path),
            ]

            # Start conversion process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            # Monitor progress if duration is available
            if duration > 0 and progress_callback:
                # Start a thread to monitor progress
                progress_thread = threading.Thread(
                    target=self.monitor_progress,
                    args=(process, duration, progress_callback, input_file),
                )
                progress_thread.daemon = True
                progress_thread.start()

            # Wait for process to complete
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                logger.info(f"Converted: {input_file} -> {output_path}")

                # Option to delete original file
                if self.delete_original:
                    os.remove(input_file)
                    logger.info(f"Deleted original file: {input_file}")

                return True
            else:
                logger.error(f"Error converting {input_file}: {stderr}")
                return False

        except Exception as e:
            logger.error(f"Unexpected error with {input_file}: {str(e)}")
            return False

    def monitor_progress(self, process, duration, callback, filename):
        """Monitor conversion progress"""
        # This is a simplified approach - in a real implementation
        # you might parse ffmpeg's stderr for more accurate progress
        start_time = time.time()

        while process.poll() is None:  # While process is running
            elapsed = time.time() - start_time
            if duration > 0:
                progress = min(100, (elapsed / duration) * 100)
                callback(filename, progress)
            time.sleep(0.5)  # Update twice per second

        # Ensure we show 100% at the end
        callback(filename, 100)

    def batch_convert(self, input_pattern="*.mp4"):
        """Convert all files matching the pattern"""
        if not self.check_ffmpeg_installed():
            logger.error("FFmpeg is not installed or not in PATH")
            return False

        files = list(glob.glob(input_pattern))

        if not files:
            logger.warning("No files found with the specified pattern")
            return False

        logger.info(f"Found {len(files)} files to convert")

        # Progress tracking
        successful = 0
        progress_bars = {}

        # Create progress bars for each file
        for file in files:
            file_size = self.get_file_size(file)
            progress_bars[file] = tqdm(
                total=100,
                desc=Path(file).name[:30].ljust(30),
                unit="%",
                bar_format="{l_bar}{bar}| {n_fmt:>3}% [{elapsed}<{remaining}]",
            )

        # Progress callback function
        def update_progress(filename, progress):
            if filename in progress_bars:
                progress_bars[filename].n = progress
                progress_bars[filename].refresh()

        # Convert each file
        for file in files:
            file_size = self.get_file_size(file)
            if self.convert_video_to_audio(file, update_progress):
                successful += 1
            progress_bars[file].close()

        logger.info(
            f"Conversion completed: {successful}/{len(files)} files successfully converted"
        )
        return successful


def main():
    parser = argparse.ArgumentParser(description="Convert MP4 video files to MP3 audio")
    parser.add_argument(
        "input",
        nargs="?",
        default="*.mp4",
        help="File pattern to convert (default: *.mp4)",
    )
    parser.add_argument(
        "-b", "--bitrate", default="192k", help="Audio bitrate (default: 192k)"
    )
    parser.add_argument(
        "-r",
        "--samplerate",
        type=int,
        default=44100,
        help="Audio sample rate (default: 44100)",
    )
    parser.add_argument("-o", "--output-dir", help="Output directory for MP3 files")
    parser.add_argument(
        "-f",
        "--format",
        default="mp3",
        choices=["mp3", "wav"],
        help="Output audio format (default: mp3)",
    )
    parser.add_argument(
        "--delete-original",
        action="store_true",
        help="Delete original files after conversion",
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing files"
    )
    parser.add_argument(
        "--list-formats", action="store_true", help="Show supported formats"
    )

    args = parser.parse_args()

    if args.list_formats:
        print("Supported input formats: mp4, mkv, avi, mov, wmv, flv, webm")
        print("Supported output formats: mp3, wav")
        return

    converter = VideoToAudioConverter(
        bitrate=args.bitrate,
        samplerate=args.samplerate,
        output_dir=args.output_dir,
        delete_original=args.delete_original,
        overwrite=args.overwrite,
        output_format=args.format,
    )

    converter.batch_convert(args.input)


if __name__ == "__main__":
    main()
