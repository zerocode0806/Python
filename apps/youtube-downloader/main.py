import os
from yt_dlp import YoutubeDL

def download_youtube_video():
    try:
        # Ask for the video URL
        video_url = input("Enter the YouTube video URL: ").strip()
        
        # Options for yt-dlp
        ydl_opts = {
            'format': 'best',  # Download the best quality
            'outtmpl': '%(title)s.%(ext)s',  # Save as video title
        }
        
        # Download the video
        with YoutubeDL(ydl_opts) as ydl:
            print("Downloading the video...")
            ydl.download([video_url])
            print("Download completed successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
download_youtube_video()
