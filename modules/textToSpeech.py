import edge_tts
import pygame
import os

async def text_to_speech(text, voice="ru-RU-DmitryNeural"):
    # Синтез речи с использованием Edge TTS и сохранение в MP3 формате
    filename = "output.mp3"
    if os.path.exists(filename):
        os.remove(filename)
    try:
        communicate = edge_tts.Communicate(text, voice=voice, rate='+20%')
        await communicate.save(filename)
        
        # Инициализация и воспроизведение MP3 файла с помощью pygame
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # Ждем окончания воспроизведения
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        # Удаляем файл после завершения воспроизведения
        os.remove(filename)
    except Exception as e:
        return e