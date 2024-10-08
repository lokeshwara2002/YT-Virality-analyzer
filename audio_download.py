import yt_dlp as youtube_dl
import logging
import os

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def download_audio(link):
    # Set up options for audio download
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': r'C:\ffmpeg\bin',  # Specify path to ffmpeg binary
        'outtmpl': 'audio.%(ext)s',  # Set output filename
    }

    logging.debug(f"Using ffmpeg location: {ydl_opts['ffmpeg_location']}")
    logging.debug(f"Options for yt-dlp: {ydl_opts}")

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            logging.info(f"Downloading audio from: {link}")
            ydl.download([link])
            logging.info("Audio downloaded successfully!")
        except Exception as e:
            logging.error(f"An error occurred: {e}", exc_info=True)

# Read the YouTube link from link.txt
link_file = 'link.txt'
if os.path.exists(link_file):
    with open(link_file, 'r') as file:
        video_link = file.read().strip()
    logging.debug(f"Read link: {video_link}")
    download_audio(video_link)
else:
    logging.error(f"Link file {link_file} does not exist")
