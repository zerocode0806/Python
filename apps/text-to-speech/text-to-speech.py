import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
import os
import pygame

# Function to preview the speech
def preview_speech():
    text = entry_text.get()
    language = var_language.get()

    if text:
        # Stop and quit pygame mixer if it's playing
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        # Save the preview audio and play it
        tts = gTTS(text=text, lang=language)
        tts.save("preview.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("preview.mp3")
        pygame.mixer.music.play()
    else:
        messagebox.showwarning("Input Error", "Please enter text to convert.")

# Function to save the speech as an MP3 file
def save_speech():
    text = entry_text.get()
    language = var_language.get()

    if text:
        # Stop pygame if the preview is playing before saving
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        tts = gTTS(text=text, lang=language)
        save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if save_path:
            tts.save(save_path)
            messagebox.showinfo("Success", "Audio file saved successfully.")
    else:
        messagebox.showwarning("Input Error", "Please enter text to convert.")

# Function to stop the preview
def stop_preview():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()

# Tkinter GUI setup
root = tk.Tk()
root.title("Text-to-Speech Converter")

# Entry for text input
tk.Label(root, text="Enter Text for TTS:").pack()
entry_text = tk.Entry(root, width=50)
entry_text.pack()

# Language selection
var_language = tk.StringVar(value="en")
tk.Radiobutton(root, text="English", variable=var_language, value="en").pack(anchor='w')
tk.Radiobutton(root, text="Indonesian", variable=var_language, value="id").pack(anchor='w')

# Buttons for preview, save, and stop
tk.Button(root, text="Preview Speech", command=preview_speech).pack()
tk.Button(root, text="Stop Preview", command=stop_preview).pack()
tk.Button(root, text="Save as MP3", command=save_speech).pack()

# Start the main event loop
root.mainloop()
