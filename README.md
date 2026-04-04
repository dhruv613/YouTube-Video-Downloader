# YT-Video-Downloader

A Python tool to download YouTube videos with flexible quality and format options.

## Features

- Download YouTube videos with customizable quality settings
- Automatic yt-dlp installation if not already installed
- Supports best quality with FFmpeg when available
- Automatic directory creation for downloads

## Requirements

- Python 3.6+
- FFmpeg (optional, for best quality merging)

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
uv pip install -r requirement.txt
```

## Usage

Edit `config.py` with your desired settings:

```python
VIDEO_URL     = "your_youtube_url_here"
OUTPUT_FOLDER = "downloads"
QUALITY       = "best"
```

Then run:

```bash
python Downloads.py
```

## Configuration

- `VIDEO_URL`: YouTube video or live stream URL
- `OUTPUT_FOLDER`: Folder where videos will be saved (default: "downloads")
- `QUALITY`: Video quality (options: "best", "worst", or specific format code)

## File Structure

- `Downloads.py` - Main downloader script
- `config.py` - Configuration settings
- `requirement.txt` - Python dependencies
- `downloads/` - Default output folder for downloaded videos
