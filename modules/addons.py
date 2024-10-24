import requests
import webbrowser
import datetime
from translate import Translator
import json

class Addons:
    def __init__(self) -> None:
        self.api_key = "0cef33e68245bf3fa8bf5147a6a330ea" # set api key for resource api
        self.xlat = Translator(to_lang="ru") # Initialization translator
        self.wdays = {
            0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday'
        } # Create a trascript for days
        with open('settings.json', encoding='utf-8') as f:
            self.data = json.load(f) # Loading settings

    def weather(self, city):
        """
        Get weather method
        Args:
            city (str): City name for weather data
        """
        url = f"http://ru.api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric" # set api link
        try:
            response = requests.get(url) # Create request to api
            response.raise_for_status()
            weather_data = response.json() # json getted weather data

            # Getting data from dict
            weather = {
                "city": weather_data["name"],
                "temperature": weather_data["main"]["temp"],
                "description": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "wind_speed": weather_data["wind"]["speed"]
            }
            
            return f'В городе {self.xlat.translate(weather['city'])} сейчас {self.xlat.translate(weather['description']).capitalize()}, {round(weather['temperature'])}°' # Return dict with sorted weather data
        except requests.exceptions.RequestException as e:
            return f"Ошибка при получении данных о погоде: {e}"
    
    def search(self, text, launch_word):
        prompt = ''
        word_list = text.split() # Create a list from string
        ind = 0
        for word in word_list:
            if word in [launch_word, 'найди', 'найти', 'привет', 'поиск']: # Check for search key in command
                del word_list[ind] # Removing it from string
            ind += 1
        prompt = ' '.join(word_list) # Compilate prompt list
        webbrowser.open(f'https://yandex.ru/search/?text={prompt}') # Open the web page with prompt
    
    def date_time(self):
        out = ''
        date = datetime.datetime.now() # Getting date
        time = list(str(date).split()[1]) # create a list for editing time
        for i in range(1,8): # Removing milliseconds
            time.pop(-1)
        out = ''.join(time) # Making string from list
        return out # Return result
    
    def timetable(self):
        print('') # Create a indent
        date = datetime.datetime.today().timetuple() # Get date and time
        table = '' # Out message
        n = 1 # Num of subject
        if date[6] == 6: # if sunday - Weekend. date[6] - day of week
            return 'Выходной'
        if date[3] > 13: # if hour > 13:00 - show table for next day
            table += '    ' + self.wdays[date[6]+1].capitalize() + '\n' # Create a heading with a day
            for i in self.data[self.wdays[date[6]+1]]: # Create the out message
                table += f'{n}) {i}\n'
            return table # Show timetable
        else:
            table += '    ' + self.wdays[date[6]].capitalize() + '\n' # Create a heading with a day
            for i in self.data[self.wdays[date[6]]]: # Create the out message for today
                table += f'{n}) {i}\n'
            return table # Show timetable
