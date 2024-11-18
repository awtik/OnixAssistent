import edge_tts
import pygame
import os
from modules.addons import Addons
import pyaudio

addns = Addons()

async def text_to_speech(text, voice="ru-RU-DmitryNeural"):
    if addns.load_settings()['tts'] == 'On':
        pygame.mixer.init()
        output_device_index = addns.load_settings().get('output_device', None)
        filename = "output.mp3"
        output_device_name = pyaudio.PyAudio().get_device_info_by_index(output_device_index).get('name')
        if output_device_index is not None:
            pygame.mixer.init(devicename=output_device_name)
        
        if os.path.exists(filename):
            os.remove(filename)
            
        try:
            communicate = edge_tts.Communicate(text, voice=voice, rate='+20%')
            await communicate.save(filename)
            
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            
        finally:
            if os.path.exists(filename):
                os.remove(filename)
    else:
        pass