import random
import json
import time
from modules.addons import Addons
from modules.music import Music
from modules.apps import open_app_by_keyword

with open('other/settings.json', encoding='utf-8') as f: # Getting settings from json
    data = json.load(f)
city = data["city"] # Setting city from settings
################################################################################################
class Commands:
    def __init__(self):
        self.wordKeys = {
            'hello_words': ['привет', 'хай', 'здарова', 'здорово'],
            'thx_words': ['спасибо', 'благодарю', 'заебись', 'отлично', 'молодец', 'прекрасно'],
            'time_words': ['время', 'часы'],
            'weather_words': ['погода', 'погоду', 'погоде', 'погодка'],
            'search_words': ['найди', 'поиск', 'поищи'],
            'exit_words': ['закройся', 'выход', 'отключись', 'пока'],
            'start_music_words': ['музыка', 'музыку'],
            'pause_music_words': ['пауза', 'приостанови', 'стоп', 'паузы', 'продолжи'],
            'next_track_words': ['следующий', 'пропусти', 'некст', 'скип', 'кип', 'следующее', 'следующая'],
            'timetable_words': ['расписание', 'уроки', 'расписанием'],
            'create_words': ['создай', 'создать', 'добавь'],
            'del_words': ['удали', 'убери', 'вычеркни', 'утолить'],
            'show_words': ['покажи', 'список']
        } # Creating key words dict for check command
        ################################################################################################
        self.addons, self.mixer, self.music = Addons(), Music(), False # Initialization Classes and set music to False
    
    def slowly_output(self, text, outlabel, delay=0.02):
        "Method for slowly output in label for output"
        outlabel.configure(text='') # Set outlabel empty
        for char in text:
            current_text = outlabel.cget('text') # Getting current text
            outlabel.configure(text=current_text + char) # Adding new char to current text
            time.sleep(delay) # Delay

    def checkwords(self, command, wordlist):
        "Check key words in command"
        command = command.split()
        for i in command:
            if i in wordlist: # if the 'i' word in the list is from the argument - return True
                return True

    def main(self, command, outlabel, app, icon_label):
        "main method"
        if 'оникс' in command: # If launch word in command - check command
            icon_label.configure(image='') # Clear weather icon
            ################################################################################################
            # Basic dialog answers
            if self.checkwords(command, self.wordKeys['hello_words']): # Check words in user voice data
                self.slowly_output(f'{random.choice(self.wordKeys['hello_words']).capitalize()}!', outlabel) # Print answer from word list
            if self.checkwords(command, self.wordKeys['thx_words']):
                self.slowly_output('Рад стараться!', outlabel)
            ################################################################################################
            # Apps open
            if command.startswith("оникс открой "): # If 'оникс открой' in command: open app
                open_app_by_keyword(command, outlabel, self.slowly_output)
            ################################################################################################
            # Functions
            if self.checkwords(command, self.wordKeys['weather_words']):
                self.slowly_output('Получаем данные о погоде...', outlabel)
                self.slowly_output(self.addons.weather(city, icon_label), outlabel) # Launch weather func from Addons class with city arg

            if self.checkwords(command, self.wordKeys['search_words']):
                self.addons.search(command, 'оникс')
                self.slowly_output('Поиск...', outlabel)

            if self.checkwords(command, self.wordKeys['time_words']):
                self.slowly_output(self.addons.date_time(), outlabel)
            ################################################################################################
            # Music
            if self.checkwords(command, self.wordKeys['start_music_words']) and not 'открой' in command:
                self.slowly_output(self.mixer.start_music(), outlabel)
                self.music = True
            if self.checkwords(command, self.wordKeys['pause_music_words']) and not 'открой' in command:
                self.mixer.pause_music()
            if self.checkwords(command, self.wordKeys['next_track_words']) and self.music:
                self.slowly_output(self.mixer.next_track(), outlabel)
            ################################################################################################
            # Timetable
            if self.checkwords(command, self.wordKeys['timetable_words']):
                self.slowly_output(self.addons.timetable(), outlabel)
            ################################################################################################
            # Exit
            if self.checkwords(command, self.wordKeys['exit_words']):
                self.slowly_output('Был рад помочь!', outlabel)
                time.sleep(1.5)
                app.destroy()
                exit()
            ################################################################################################
        if self.music and not self.mixer.pause: # Check active track
            self.mixer.check_music()