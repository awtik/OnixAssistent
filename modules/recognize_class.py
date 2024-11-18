import json
import pyaudio
import os
import shutil
from vosk import Model, KaldiRecognizer
from modules.addons import Addons

addns = Addons()

class Recognize:
    def __init__(self):
        try:
            self.model = Model("C:/Onix/model")
        except:
            model_project_path = f"{os.path.abspath(os.curdir)}/model"
            model_new_location = "C:/Onix/model"
            shutil.copytree(model_project_path, model_new_location)
            self.model = Model(model_new_location)

        # Загрузка настроек устройства ввода
        input_device_index = addns.load_settings().get('input_device', 0)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000,
                                      input=True,
                                      frames_per_buffer=8000,
                                      input_device_index=input_device_index)
        os.system('cls')

    def recognize_speech(self, label, cmnds, outlabel, app, slowly_output, icon_label):
        try:
            while True:
                data = self.stream.read(4000, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    if "text" in result:
                        slowly_output(result['text'].capitalize(), label)
                        cmnds.handle_command(result['text'].lower(), outlabel, app, icon_label)
        except KeyboardInterrupt:
            print("Speech recognition stopped.")
        finally:
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()