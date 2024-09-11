from modules.recognizeClass import Recognize
from modules.gptResponse import get_answer, show_answers
from modules.addons import Addons
from modules.music import Music
from modules.sql import Database
from modules.tasks import Tasks
import random

################################################################################################
wordKeys = {
    'hello_words': ['привет', 'хай', 'здарова', 'здорово'],
    'thx_words': ['спасибо', 'благодарю', 'заебись', 'отлично', 'молодец', 'прекрасно'],
    'time_words': ['время', 'часы'],
    'weather_words': ['погода', 'погоду', 'погоде', 'погодка'],
    'gpt_words': ['запрос', 'генерация', 'придумай', 'придумать', 'придумали', 'создай'],
    'search_words': ['найди', 'поиск', 'поищи'],
    'exit_words': ['закройся', 'выход', 'отключись', 'пока'],
    'start_music_words': ['музыка', 'музыку'],
    'pause_music_words': ['пауза', 'приостанови', 'стоп', 'паузы', 'продолжи'],
    'next_track_words': ['следующий', 'пропусти', 'некст', 'скип', 'кип', 'следующее', 'следующая'],
    'task_words': ['задачу', 'задачку', 'задач', 'задачи', 'задача'],
    'create_words': ['создай', 'создать', 'добавь'],
    'del_words': ['удали', 'убери', 'вычеркни', 'утолить'],
    'show_words': ['покажи', 'список']
} # Creating key words dict for check command
################################################################################################

class Assistent:
    def __init__(self):
        "Initialization classes"
        self.addons = Addons() # Initialization Addons class
        self.r = Recognize() # Initialization recognizer
        self.mixer = Music() # Initialization music class
        self.db = Database() # Initialization gpt db
        self.tsks = Tasks() # Initialization tasks class
        self.music = False

    def checkwords(self, command, wordlist):
        "Check key words in command"
        command = command.split()
        for i in command:
            if i in wordlist:
                return True
            
    def main(self):
        "main method"
        print('Ожидание ввода...')
        command = self.r.recognize_speech() # recognize voice data
        print(f'Command: {command}') # Print recognized data
        if 'оникс' in command:
            ################################################################################################
            # Basic dialog answers
            if self.checkwords(command, wordKeys['hello_words']): # Check words in user voice data
                print(f'{random.choice(wordKeys['hello_words']).capitalize()}!') # Print answer from word list
            if self.checkwords(command, wordKeys['thx_words']):
                print('Рад стараться!')
            ################################################################################################
            # Functions
            if self.checkwords(command, wordKeys['weather_words']):
                self.addons.weather('Кропоткин') # Launch weather func from Addons class with city arg

            if self.checkwords(command, wordKeys['gpt_words']) and not self.checkwords(command, wordKeys['task_words']):
                print(get_answer(command)) # Print gpt answer

            if 'запросы' in command:
                show_answers() # Show all gpt responses
            
            if self.checkwords(command, wordKeys['search_words']):
                self.addons.search(command)
            
            if self.checkwords(command, wordKeys['time_words']):
                print(self.addons.date_time())
            ################################################################################################
            # Tasks
            if self.checkwords(command, wordKeys['task_words']) and self.checkwords(command, wordKeys['create_words']):
                self.tsks.task_create(command)
            if self.checkwords(command, wordKeys['del_words']) and self.checkwords(command, wordKeys['task_words']):
                self.tsks.task_remove(command)
            if self.checkwords(command, wordKeys['task_words']) and self.checkwords(command, wordKeys['show_words']):
                print(self.tsks.show_tasks())
            ################################################################################################
            # Music
            if self.checkwords(command, wordKeys['start_music_words']):
                self.mixer.start_music()
                self.music = True
            if self.checkwords(command, wordKeys['pause_music_words']):
                self.mixer.pause_music()
            if self.checkwords(command, wordKeys['next_track_words']) and self.music:
                self.mixer.next_track()
            ################################################################################################
            # Exit
            if self.checkwords(command, wordKeys['exit_words']):
                print('Был рад помочь!')
                exit()
            ################################################################################################
            # Unknown command
                print('Неизвестная команда!')

        if self.music and not self.mixer.pause: # Check active track
            self.mixer.check_music()
            
ass = Assistent()
while(1):
    ass.main() # Launch