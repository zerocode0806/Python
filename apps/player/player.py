import os
import pygame
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip
from tkinter import messagebox
from PIL import Image, ImageTk
import shutil  # For deleting temporary files
import time

# Initialize Pygame mixer for audio
pygame.mixer.init()

# Define the media player class
class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Media Player")
        self.root.geometry("500x400")
        self.playlist = []  # List of media files
        self.current_index = 0  # Track current song index
        self.current_video = None  # Store the currently opened video file
        self.temp_audio_path = "temp_audio.mp3"  # Temp audio path

        # UI Elements
        self.title_label = tk.Label(self.root, text="Media Player", font=("Helvetica", 15))
        self.title_label.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_media, width=10)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_media, width=10)
        self.pause_button.pack(pady=5)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_media, width=10)
        self.next_button.pack(pady=5)

        self.previous_button = tk.Button(self.root, text="Previous", command=self.previous_media, width=10)
        self.previous_button.pack(pady=5)

        self.forward_button = tk.Button(self.root, text="Forward 5s", command=self.forward_media, width=10)
        self.forward_button.pack(pady=5)

        self.backward_button = tk.Button(self.root, text="Backward 5s", command=self.backward_media, width=10)
        self.backward_button.pack(pady=5)

        self.add_button = tk.Button(self.root, text="Add File", command=self.add_media, width=10)
        self.add_button.pack(pady=5)

        self.now_playing_label = tk.Label(self.root, text="Now Playing: None", font=("Helvetica", 10))
        self.now_playing_label.pack(pady=10)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Scale(self.root, variable=self.progress_var, from_=0, to=100, orient="horizontal", length=400)
        self.progress_bar.pack(pady=10)

        # Thumbnail label
        self.thumbnail_label = tk.Label(self.root)
        self.thumbnail_label.pack(pady=10)

        # Initialize variables for media
        self.is_paused = False
        self.current_file = None

        # Start updating the progress bar
        self.update_progress()

    def add_media(self):
        # Open file dialog to select a media file (mp3, wav, mp4, etc.)
        file_path = filedialog.askopenfilename(filetypes=[("Audio/Video Files", "*.mp3 *.wav *.mp4 *.avi *.mkv")])
        if file_path:
            self.playlist.append(file_path)
            messagebox.showinfo("File Added", f"Added {os.path.basename(file_path)} to playlist")

    def play_media(self):
        if self.playlist:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                file = self.playlist[self.current_index]
                self.load_media(file)
        else:
            messagebox.showwarning("Empty Playlist", "Please add a media file first.")

    def pause_media(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True

    def next_media(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.load_media(self.playlist[self.current_index])

    def previous_media(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.load_media(self.playlist[self.current_index])

    def forward_media(self):
        if pygame.mixer.music.get_busy():
            current_pos = pygame.mixer.music.get_pos() / 1000  # Get current position in seconds
            pygame.mixer.music.set_pos(current_pos + 5)  # Forward 5 seconds

    def backward_media(self):
        if pygame.mixer.music.get_busy():
            current_pos = pygame.mixer.music.get_pos() / 1000
            pygame.mixer.music.set_pos(max(0, current_pos - 5))  # Backward 5 seconds

    def load_media(self, file):
        # Stop any current media
        pygame.mixer.music.stop()

        # Extract audio if the file is a video (mp4, avi, mkv, etc.)
        if file.endswith(('.mp4', '.avi', '.mkv')):
            self.extract_audio(file)
        else:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            self.update_now_playing(file)

    def extract_audio(self, file):
        # Use moviepy to extract the audio from the video file
        if self.current_video:
            self.current_video.close()  # Close any previously opened video file

        try:
            self.current_video = VideoFileClip(file)
            audio_path = self.temp_audio_path
            
            # Extract and write audio, and close it explicitly
            with self.current_video.audio as audio_clip:
                audio_clip.write_audiofile(audio_path)

            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            self.update_now_playing(file)
            self.update_thumbnail(file)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading video: {str(e)}")
        finally:
            # Ensure the ffmpeg process and video resources are closed properly
            if self.current_video:
                try:
                    self.current_video.close()  # Close video to release resources
                except Exception as e:
                    print(f"Error closing video: {str(e)}")
            self.cleanup_ffmpeg_process()

    def update_now_playing(self, file):
        self.now_playing_label.config(text=f"Now Playing: {os.path.basename(file)}")
        self.update_thumbnail(file)

    def update_thumbnail(self, file):
        # Display thumbnail for video files
        if file.endswith(('.mp4', '.avi', '.mkv')):
            try:
                frame = self.current_video.get_frame(0)  # Get the first frame from the currently opened video
                frame_image = Image.fromarray(frame)
                frame_image.thumbnail((200, 200))  # Resize the image
                self.thumbnail = ImageTk.PhotoImage(frame_image)
                self.thumbnail_label.config(image=self.thumbnail)
            except Exception as e:
                self.thumbnail_label.config(image="")
                print(f"Error loading thumbnail: {e}")
        else:
            self.thumbnail_label.config(image="")  # Clear the thumbnail for audio files

    def update_progress(self):
        if pygame.mixer.music.get_busy():
            current_pos = pygame.mixer.music.get_pos() / 1000  # Get current position in seconds
            total_length = self.get_total_length()
            if total_length > 0:
                self.progress_var.set((current_pos / total_length) * 100)  # Update the progress bar
        self.root.after(1000, self.update_progress)  # Update every second

    def get_total_length(self):
        # Get total length of the current media file
        if self.playlist:
            file = self.playlist[self.current_index]
            if file.endswith(('.mp3', '.wav')):
                audio_file = pygame.mixer.Sound(file)
                return audio_file.get_length()
            elif file.endswith(('.mp4', '.avi', '.mkv')) and self.current_video:
                return self.current_video.duration
        return 0

    def cleanup(self):
        # Remove temporary audio file if it exists
        if os.path.exists(self.temp_audio_path):
            os.remove(self.temp_audio_path)

    def cleanup_ffmpeg_process(self):
        """Clean up any remaining ffmpeg process to avoid lingering file handles."""
        try:
            if hasattr(self.current_video, 'audio') and self.current_video.audio:
                self.current_video.audio.close()
        except Exception as e:
            print(f"Error cleaning up ffmpeg process: {e}")

# Create the root window and MediaPlayer instance
root = tk.Tk()
player = MediaPlayer(root)

# Ensure cleanup when the window is closed
root.protocol("WM_DELETE_WINDOW", player.cleanup)

# Run the Tkinter main loop
root.mainloop()
