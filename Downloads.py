import subprocess
import sys
import os
import shutil
import config

class Download:     

    def install_ytdlp():
        """Install yt-dlp if not already installed."""
        try:
            import yt_dlp
            print("✅ yt-dlp is already installed.")
        except ImportError:
            print("📦 Installing yt-dlp...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            print("✅ yt-dlp installed successfully.")

    def download_video(url, output_folder="downloads", quality="best"):
        """
        Download a YouTube video.
        """    
        import yt_dlp

        os.makedirs(output_folder, exist_ok=True)

        ffmpeg_available = shutil.which("ffmpeg") is not None

        # Use merge formats only when ffmpeg exists.
        format_map_ffmpeg = {
            "best":   "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "medium": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]/best",
            "audio":  "bestaudio/best",
        }
        # Fallback to single-file formats when ffmpeg is missing.
        format_map_no_ffmpeg = {
            "best":   "best[ext=mp4]/best",
            "medium": "best[height<=720][ext=mp4]/best[height<=720]/best",
            "audio":  "bestaudio[ext=m4a]/bestaudio/best",
        }

        selected_format = (
            format_map_ffmpeg if ffmpeg_available else format_map_no_ffmpeg
        ).get(quality, format_map_ffmpeg["best"] if ffmpeg_available else format_map_no_ffmpeg["best"])

        ydl_opts = {
            "format": selected_format,
            "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
            "noplaylist": True,
            "progress_hooks": [Download.progress_hook],
        }

        if ffmpeg_available:
            ydl_opts["merge_output_format"] = "mp4"
        else:
            print("⚠️ ffmpeg not found. Using non-merge fallback formats.")

        # For audio-only, convert to mp3 only when ffmpeg exists.
        if quality == "audio" and ffmpeg_available:
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        elif quality == "audio":
            print("⚠️ ffmpeg not found. Audio will be downloaded in source format (for example .m4a/webm).")

        print(f"\n🎬 Starting download...")
        print(f"📁 Saving to: {os.path.abspath(output_folder)}\n")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "Unknown")
            print(f"\n✅ Download complete: '{title}'")


    def progress_hook(d):
        """Show download progress."""
        if d["status"] == "downloading":
            percent = d.get("_percent_str", "?%").strip()
            speed   = d.get("_speed_str", "? KB/s").strip()
            eta     = d.get("_eta_str", "?").strip()
            print(f"\r⬇️  {percent}  |  Speed: {speed}  |  ETA: {eta}   ", end="", flush=True)
        elif d["status"] == "finished":
            print(f"\n🔄 Processing file...")


if __name__ == "__main__":

    Download.install_ytdlp()
    Download.download_video(config.VIDEO_URL, config.OUTPUT_FOLDER, config.QUALITY)
