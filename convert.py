# A script to convert video files to audio files using FFmpeg.
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
    handlers=[logging.FileHandler(
        "conversion.log"), logging.StreamHandler(sys.stdout)],
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

        # Supported formats
        self.supported_input_formats = {
            ".mp4",
            ".mkv",
            ".avi",
            ".mov",
            ".wmv",
            ".flv",
            ".webm",
        }
        self.supported_output_formats = {"mp3", "wav"}

        if output_dir:
            Path(output_dir).mkdir(parents=True, exist_ok=True)

    def check_ffmpeg_installed(self):
        try:
            subprocess.run(["ffmpeg", "-version"],
                           capture_output=True, check=True)
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
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except Exception:
            return 0

    def convert_video_to_audio(self, input_file, progress_callback=None):
        input_path = Path(input_file)

        # Check if input format is supported
        if input_path.suffix.lower() not in self.supported_input_formats:
            logger.error(f"Formato input non supportato: {input_path.suffix}")
            logger.error(
                f"Formati supportati: {
                    ', '.join(self.supported_input_formats)}"
            )
            return False

        # Check if output format is supported
        if self.output_format not in self.supported_output_formats:
            logger.error(f"Formato output non supportato: {
                         self.output_format}")
            logger.error(
                f"Formati supportati: {
                    ', '.join(self.supported_output_formats)}"
            )
            return False

        # Determine output path
        if self.output_dir:
            output_path = Path(self.output_dir) / (
                input_path.stem + f".{self.output_format}"
            )
        else:
            output_path = input_path.with_suffix(f".{self.output_format}")

        if output_path.exists() and not self.overwrite:
            logger.warning(f"{output_path} exists, skipping.")
            return False

        duration = self.get_video_duration(input_file)

        # Build FFmpeg command based on output format
        if self.output_format == "mp3":
            audio_codec = "libmp3lame"
        elif self.output_format == "wav":
            audio_codec = "pcm_s16le"
        else:
            audio_codec = "libmp3lame"  # default

        cmd = [
            "ffmpeg",
            "-i",
            str(input_file),
            "-vn",  # no video
            "-acodec",
            audio_codec,
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
    input_file,
    output_file=None,
    bitrate="192k",
    samplerate=44100,
    overwrite=False,
    output_format="mp3",
):
    converter = VideoToAudioConverter(
        bitrate=bitrate,
        samplerate=samplerate,
        overwrite=overwrite,
        output_format=output_format,
    )
    return converter.convert_video_to_audio(input_file)


# === MAIN EXECUTION ===
if __name__ == "__main__":
    print("🎵 VIDEO TO AUDIO CONVERTER 🎵")
    print("=" * 50)

    # Verifica FFmpeg
    converter = VideoToAudioConverter()
    if not converter.check_ffmpeg_installed():
        print("❌ ERRORE: FFmpeg non trovato!")
        print("Installa FFmpeg da: https://ffmpeg.org/download.html")
        sys.exit(1)

    # Cerca file video supportati nella cartella
    video_files = []
    for fmt in converter.supported_input_formats:
        video_files.extend(Path(".").glob(f"*{fmt}"))
        video_files.extend(Path(".").glob(f"*{fmt.upper()}"))

    if not video_files:
        print("❌ Nessun file video supportato trovato!")
        print("Formati supportati:")
        for fmt in converter.supported_input_formats:
            print(f"  - {fmt}")
        print(f"\nInserisci un file video in questa cartella:")
        print(f"  {os.getcwd()}")
        sys.exit(1)

    # Seleziona file
    if len(video_files) == 1:
        video_file = str(video_files[0])
        print(f"📹 Trovato file: {video_file}")
    else:
        print("📹 File video trovati:")
        for i, file in enumerate(video_files, 1):
            print(f"  {i}. {file.name}")

        try:
            scelta = int(
                input("\nScegli il numero del file da convertire: ")) - 1
            video_file = str(video_files[scelta])
        except (ValueError, IndexError):
            print("❌ Scelta non valida!")
            sys.exit(1)

    # Seleziona formato output
    print("\n🎵 Formati output disponibili:")
    print("  1. MP3 (consigliato)")
    print("  2. WAV (qualità superiore)")

    try:
        formato_scelta = input(
            "Scegli il formato output (1-2, default: 1): ").strip()
        if formato_scelta == "2":
            output_format = "wav"
            bitrate = "320k"  # Migliore qualità per WAV
        else:
            output_format = "mp3"
            bitrate = "192k"
    except:
        output_format = "mp3"
        bitrate = "192k"

    # Configura il convertitore
    converter = VideoToAudioConverter(
        output_dir="converted_audio",
        overwrite=True,
        bitrate=bitrate,
        output_format=output_format,
    )

    # Funzione per mostrare il progresso
    def show_progress(filename, progress):
        if progress == 100:
            print(f"✅ {Path(filename).name} - Completato!")
        elif progress % 25 == 0:
            print(f"🔄 {Path(filename).name} - {progress:.1f}%")

    # Converti!
    print(f"\n🎬 Convertendo {
          Path(video_file).name} -> {output_format.upper()}...")
    print("⏳ Questo potrebbe richiedere alcuni minuti...")

    success = converter.convert_video_to_audio(video_file, show_progress)

    if success:
        print("\n🎉 CONVERSIONE COMPLETATA!")
        output_filename = Path(video_file).stem + f".{output_format}"
        print(f"📁 File salvato in: converted_audio/{output_filename}")
    else:
        print("\n❌ CONVERSIONE FALLITA!")
        print("📄 Controlla il file 'conversion.log' per dettagli sull'errore")
