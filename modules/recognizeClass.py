import json
import pyaudio
from vosk import Model, KaldiRecognizer
import os
import shutil

class Recognize:
    def __init__(self):
        """Preparing to recognize"""
        try:
            model = Model("C:/Onix/model") # Try to loading model
        except: # If Error: create model folder in C:/
            model_project_path = f"{os.path.abspath(os.curdir)}/model" # Find model in project folder
            model_new_location = "C:/Onix/model" # Set new path for model
            shutil.copytree(model_project_path, model_new_location) # Copy model from project to new path
            model = Model(model_new_location) # Loading model again
        self.recognizer = KaldiRecognizer(model, 16000) # Create a translator
        audio = pyaudio.PyAudio()
        self.stream = audio.open(format=pyaudio.paInt16, # Create a voice stream
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=8000)
        os.system('cls') # CLear model loading text
    
    def recognize_speech(self, label, cmnds, outlabel, app, slowly_output, icon_label):
        """Recognize method"""
        while(1):
            data = self.stream.read(4000, exception_on_overflow = False) # Listen
            if len(data) == 0: # If user said nothing - pass
                pass
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result()) # Load recognized data to json
                if "text" in result:
                    slowly_output(result['text'].capitalize(), label) # Edit label with user input
                    cmnds.main(result['text'].lower(), outlabel, app, icon_label) # Start checkcommand func