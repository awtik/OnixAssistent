import json
import pyaudio
from vosk import Model, KaldiRecognizer
import os

class Recognize:
    def __init__(self):
        """Preparing to recognize"""
        model = Model("VoiceAssistent/model") # Loading model
        self.recognizer = KaldiRecognizer(model, 16000) # Create a translator
        audio = pyaudio.PyAudio()
        self.stream = audio.open(format=pyaudio.paInt16, # Create a voice stream
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=8000)
        os.system('cls') # CLear model loading text
    
    def recognize_speech(self):
        """Recognize method"""
        while(1):
            data = self.stream.read(4000, exception_on_overflow = False) # Listen
            if len(data) == 0: # If user said nothing - pass
                pass
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result()) # Load recognized data to json
                if "text" in result:
                    return result['text'] # Return recognized text