import pygame
import os
import random

pygame.mixer.init()
pygame.init()

class Music:
    def __init__(self):
        "Initialization method"
        self.folder_path = f'{os.path.abspath(os.getcwd())}/tracks' # Set music folder
        self.audio_extensions = ['.mp3', '.wav', '.ogg', '.flac'] # Set music extensions
        self.files = [file for file in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, file)) and
                os.path.splitext(file)[1].lower() in self.audio_extensions] # Create a list with all songs
        self.current_song_index = 0 # Index of song
        self.pause = False
    
    def play_music(self, path):
        "Start music method"
        pygame.mixer.music.load(path) # Load track
        pygame.mixer.music.play() # Play track

    def start_music(self):
        "Start music method"
        if pygame.mixer.music.get_busy() or self.pause:
            self.pause_music()
        else:
            random.shuffle(self.files) # shuffle track list
            file_path = os.path.join(self.folder_path, self.files[self.current_song_index]) # Create a path to music ile
            print(f"Playing: {self.files[self.current_song_index]}") # Print name of current track
            self.play_music(file_path) # Play music
    
    def check_music(self):
        "Check playing music method"
        if not pygame.mixer.music.get_busy(): # If not music now - play next
            random.shuffle(self.files) # Shuffle track list
            self.current_song_index = (self.current_song_index + 1) % len(self.files) # Set new song index
            file_path = os.path.join(self.folder_path, self.files[self.current_song_index]) # Set new path to file
            self.play_music(file_path) # Play music

    def next_track(self):
        "Next track select method"
        self.current_song_index = (self.current_song_index + 1) % len(self.files) # Set new song index
        file_path = os.path.join(self.folder_path, self.files[self.current_song_index]) # Set new path to file
        self.play_music(file_path) # Play music

    def pause_music(self):
        "Pause/unpause method"
        if not self.pause:
            pygame.mixer.music.pause() # Pause
            self.pause = True
        else:
            pygame.mixer.music.unpause()
            self.pause = False # Unpause