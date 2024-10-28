import edge_tts
import asyncio
import os

async def text_to_speech(text, voice="ru-RU-DmitryNeural"):
    # Синтез речи с использованием Edge TTS и выбранного голоса
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save("output.mp3")

    # Воспроизведение аудиофайла (Windows)
    os.system("start output.mp3")

# Вызов синтеза речи с мужским голосом
text = "Привет, сегодня облачно"
asyncio.run(text_to_speech(text))