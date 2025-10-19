# 🎬 ConvertPy — Video to Audio Converter
A lightweight Python script to convert video files (like `.mp4`) into audio files (`.mp3` or `.wav`) using **FFmpeg**. Includes logging, progress tracking, and customizable output settings.
---
## ⚙️ Features
- 🎧 Convert video → audio (`.mp3` or `.wav`)
- 📊 Progress tracking during conversion
- 🧩 Configurable bitrate, sample rate, and output directory
- 🔁 Option to overwrite existing files
- 🗑️ Option to delete original video files after conversion
- 🧾 Detailed logging (`conversion.log`)
- 🧠 Simple class-based design for easy reuse in other projects
---
## 🧰 Requirements
- **Python 3.8+**
- **FFmpeg** and **FFprobe** installed and accessible in your system `PATH`
- Optional: [`tqdm`](https://pypi.org/project/tqdm/) for enhanced progress display (not required)
---
## 📦 Installation
```bash
# Clone the repository
git clone https://github.com/Ayanashi/ConvertPy.git
cd ConvertPy

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install optional dependencies
pip install tqdm
```
Make sure FFmpeg is installed and works:
```bash
ffmpeg -version
ffprobe -version
```
If not, install it from your package manager or from [ffmpeg.org/download.html](https://ffmpeg.org/download.html).
---
## 🚀 Usage
### 🔹 Basic Example
```bash
python convert.py
```
The script will:
1. Look for supported video files in the current directory  
2. Ask for the desired output format (MP3 or WAV)  
3. Convert the file and show progress  
4. Save output in the same or specified directory  
---
### 🔹 Programmatic Use (as a module)
```python
from convert import VideoToAudioConverter, convert_to_audio

converter = VideoToAudioConverter(
    bitrate="192k",
    samplerate=44100,
    output_dir="converted_audio",
    overwrite=True,
    delete_original=False,
    output_format="mp3"
)

success = converter.convert_video_to_audio("example.mp4")

if success:
    print("✅ Conversion successful!")
else:
    print("❌ Conversion failed.")
```
You can also use the helper function:
```python
convert_to_audio("input.mp4", bitrate="192k", samplerate=44100, overwrite=True)
```
---
## ⚙️ Parameters
| Parameter | Description | Default |
|------------|-------------|----------|
| `bitrate` | Audio bitrate (e.g., `192k`, `256k`) | `"192k"` |
| `samplerate` | Audio sample rate (e.g., `44100`, `48000`) | `44100` |
| `output_dir` | Directory where output audio files are saved | `None` |
| `delete_original` | Delete the original video after conversion | `False` |
| `overwrite` | Overwrite existing files | `False` |
| `output_format` | Output format (`"mp3"` or `"wav"`) | `"mp3"` |
---
## 🧾 Logging
All events are logged to `conversion.log` — including successful conversions, skipped files, and errors.
Example log entry:
```
2025-10-19 21:22:11 - INFO - Converted: video.mp4 -> converted_audio/video.mp3
```
---
## 🧩 Supported Formats
| Type | Extensions |
|------|-------------|
| Input | `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm` |
| Output | `.mp3`, `.wav` |
---
## 🐛 Troubleshooting
- **FFmpeg not found:** Make sure it’s installed and in your system PATH.  
- **Conversion skipped:** The output file already exists and `overwrite=False`.  
- **Progress not updating:** Timer-based progress is approximate and depends on system performance.  
- **Corrupted output:** Check bitrate and samplerate settings, or try with WAV output.  
---
## 🧠 Example Output
```
🎵 Converting: example.mp4 → example.mp3
Progress: 25%
Progress: 50%
Progress: 75%
✅ Conversion complete!
```
Output file: `converted_audio/example.mp3`
---
## 🧑‍💻 Author
Developed by [**Ayanashi**](https://github.com/Ayanashi)  
Feel free to open an issue or pull request if you find bugs or want to contribute.
---
## 📜 License
This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.  
You are free to use, modify, and distribute this software under the terms of the GPLv3.  
See the [LICENSE](LICENSE) file for full details.
