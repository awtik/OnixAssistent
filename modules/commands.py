import random
import time
import asyncio
from modules.addons import Addons
from modules.apps import open_app_by_keyword
from modules.text_to_speech import text_to_speech

class Commands:
    def __init__(self):
        self.wordKeys = {
            'hello_words': ['привет', 'хай'],
            'thx_words': ['спасибо', 'благодарю', 'отлично', 'молодец'],
            'time_words': ['время', 'часы'],
            'weather_words': ['погода', 'погоду', 'погоде', 'погодка'],
            'search_words': ['найди', 'поиск', 'поищи'],
            'exit_words': ['закройся', 'выход', 'отключись', 'пока'],
            'timetable_words': ['расписание', 'уроки', 'расписанием', 'расписанию'],
            'del_words': ['удали', 'убери', 'вычеркни', 'утолить'],
            'open_words': ['открой', 'запусти', 'открыть']
        }
        self.addons = Addons()
        data = self.addons.load_settings()
        self.city = data["city"]

    def slowly_output(self, text, outlabel, delay=0.01):
        outlabel.configure(text='')
        for char in text:
            current_text = outlabel.cget('text')
            outlabel.configure(text=current_text + char)
            time.sleep(delay)

    def check_words(self, command, wordlist):
        command = command.split()
        return any(i in wordlist for i in command)

    def handle_command(self, command, outlabel, app, icon_label):
        if 'оникс' in command:
            icon_label.configure(image='')

            if self.check_words(command, self.wordKeys['hello_words']):
                text = f'{random.choice(self.wordKeys["hello_words"]).capitalize()}!'
                self.slowly_output(text, outlabel)
                asyncio.run(text_to_speech(text))

            if self.check_words(command, self.wordKeys['thx_words']):
                response_text = 'Рад стараться!'
                self.slowly_output(response_text, outlabel)
                asyncio.run(text_to_speech(response_text))

            if self.check_words(command, self.wordKeys['open_words']):
                text = open_app_by_keyword(command, outlabel, self.slowly_output)
                self.slowly_output(text, outlabel)
                asyncio.run(text_to_speech(text))

            if self.check_words(command, self.wordKeys['weather_words']):
                self.slowly_output('Получаем данные о погоде...', outlabel)
                weather = self.addons.weather_output(self.city, icon_label)
                self.slowly_output(weather, outlabel)
                asyncio.run(text_to_speech(weather))

            if self.check_words(command, self.wordKeys['search_words']):
                self.addons.search(command, 'оникс')
                self.slowly_output('Поиск...', outlabel)
                asyncio.run(text_to_speech('Поиск'))

            if self.check_words(command, self.wordKeys['time_words']):
                current_time = self.addons.time()
                self.slowly_output(current_time, outlabel)
                asyncio.run(text_to_speech(current_time))

            if self.check_words(command, self.wordKeys['timetable_words']):
                text = self.addons.timetable()
                self.slowly_output(text, outlabel)
                asyncio.run(text_to_speech(text))

            if self.check_words(command, self.wordKeys['exit_words']):
                farewell_text = 'Был рад помочь!'
                self.slowly_output(farewell_text, outlabel)
                asyncio.run(text_to_speech(farewell_text))
                time.sleep(1.5)
                app.destroy()
                exit()

async def main_loop(command, outlabel, app, icon_label):
    commands = Commands()
    await commands.handle_command(command, outlabel, app, icon_label)