import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from gtts import gTTS
import pyttsx3
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

# Initialize pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

# Function to play text in real-time using pyttsx3
def play_text():
    text = text_input.get("1.0", "end-1c")  # Get text from the input box
    voice_gender = voice_var.get()  # Get selected voice gender

    if not text.strip():
        messagebox.showwarning("Input Error", "Please enter some text!")
        return

    try:
        # Set voice based on gender
        voices = engine.getProperty('voices')
        if voice_gender == 'male':
            engine.setProperty('voice', voices[0].id)  # Male voice
        else:
            engine.setProperty('voice', voices[1].id)  # Female voice

        # Speak the text
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to save text as MP3 and play it
def save_and_play():
    global mp3_file_path  # Store the file path globally
    text = text_input.get("1.0", "end-1c")  # Get text from the input box
    voice_gender = voice_var.get()  # Get selected voice gender
    save_location = file_path_var.get()  # Get file save location

    if not text.strip():
        messagebox.showwarning("Input Error", "Please enter some text!")
        return

    if not save_location:
        messagebox.showwarning("Save Error", "Please choose a file location to save the MP3!")
        return

    try:
        # Save the speech as an MP3 file using gTTS
        tts = gTTS(text=text, lang='hi')  # Change 'hi' to 'en' for English
        mp3_file_path = save_location  # Save the file path globally
        tts.save(mp3_file_path)
        messagebox.showinfo("Success", f"Speech saved as {mp3_file_path}")

        # Play the saved MP3 file using pygame.mixer
        pygame.mixer.music.load(mp3_file_path)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to choose file save location
def choose_file_location():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3 Files", "*.mp3")],
        title="Save MP3 File"
    )
    if file_path:
        file_path_var.set(file_path)

# Create the main window
root = tk.Tk()
root.title("Text-to-Speech Converter")
root.geometry("600x450")
root.resizable(False, False)

# Modern theme
style = ttk.Style()
style.theme_use("clam")

# Text input box
tk.Label(root, text="Enter Text:", font=("Arial", 12)).pack(pady=5)
text_input = tk.Text(root, height=10, width=60, font=("Arial", 11))
text_input.pack(pady=10)

# Voice persona selection
tk.Label(root, text="Select Voice Persona:", font=("Arial", 12)).pack(pady=5)
voice_var = tk.StringVar(value="female")
voice_frame = ttk.Frame(root)
voice_frame.pack()
ttk.Radiobutton(voice_frame, text="Male", variable=voice_var, value="male").pack(side="left", padx=10)
ttk.Radiobutton(voice_frame, text="Female", variable=voice_var, value="female").pack(side="left", padx=10)

# File save location
tk.Label(root, text="Save MP3 File Location:", font=("Arial", 12)).pack(pady=5)
file_path_var = tk.StringVar()
file_frame = ttk.Frame(root)
file_frame.pack()
ttk.Entry(file_frame, textvariable=file_path_var, width=50, font=("Arial", 11)).pack(side="left", padx=5)
ttk.Button(file_frame, text="Browse", command=choose_file_location).pack(side="left", padx=5)

# Play and Save buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)
ttk.Button(button_frame, text="Play Text", command=play_text).pack(side="left", padx=10)
ttk.Button(button_frame, text="Save & Play MP3", command=save_and_play).pack(side="left", padx=10)

# Run the application
root.mainloop()