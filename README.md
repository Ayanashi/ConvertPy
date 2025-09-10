# ConverTpy 🎵

A simple Python tool to convert video files to audio format with progress bars.

## Quick Start

1. **Install FFmpeg** on your system
2. **Install dependency**: `pip install tqdm`
3. **Run converter**: `python convert.py`

## Basic Usage

# Convert all MP4 files in current folder
`python convert.py`

# Convert specific files
`python convert.py video1.mp4 video2.mkv`

# Save to custom folder
`python convert.py -o audio_output/`

# High quality conversion
`python convert.py -b 320k`

# Convert to WAV format
`python convert.py -f wav`

## Supported Formats

Input: mp4, mkv, avi, mov, wmv, flv, webm  
Output: mp3, wav

## Options

-b, --bitrate - Audio quality (default: 192k)  
-f, --format - Output format: mp3 or wav  
-o, --output-dir - Custom output folder  
--delete-original - Remove original files after conversion  
--overwrite - Replace existing files  
--list-formats - Show supported formats

## Examples

# Convert with high quality and delete originals
`python convert.py -b 320k --delete-original`

# Convert to WAV format in custom folder
`python convert.py -f wav -o my_audio/`

# Convert specific files with overwrite
`python convert.py video1.mp4 video2.mov --overwrite`

# Show supported formats
`python convert.py --list-formats`

## Requirements

Python 3.6+  
FFmpeg installed  
tqdm library (pip install tqdm)

## Troubleshooting

FFmpeg not found error:  
Make sure FFmpeg is installed and available in your system PATH.


Permission errors:  
Run with appropriate permissions or choose a different output directory.
