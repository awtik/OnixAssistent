import requests
import webbrowser
import datetime
from translate import Translator
import json
from io import BytesIO
from PIL import Image
from customtkinter import CTkImage

class Addons:
    def __init__(self):
        "Init method"
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
        with open('other/settings.json', encoding='utf-8') as f:
            self.data = json.load(f) # Loading settings

    def weather(self, city, icon_label):
        "Get weather method"
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
                "wind_speed": weather_data["wind"]["speed"],
                "icon": weather_data["weather"][0]["icon"]
            }
            
            icon_code = weather["icon"] # Get icon code
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png" # Create url for get image from code
            response = requests.get(icon_url) # Get image
            img_data = response.content # Get image from data
            img = Image.open(BytesIO(img_data)) # Create image from bytes
            img = CTkImage(img, size=(80,80))

            icon_label.configure(image=img) # Edit label to icon
            icon_label.image = img # Set image

            return f'В городе {self.xlat.translate(weather['city'])} сейчас \n{self.xlat.translate(weather['description']).capitalize()}, {round(weather['temperature'])}° | {weather['description']}' # Return dict with sorted weather data
        except requests.exceptions.RequestException as e: # If error: return error
            return f"Ошибка при получении данных о погоде: {e}"
    
    def search(self, text, launch_word):
        "Method for search in browser"
        keywords = {launch_word, 'найди', 'найти', 'привет', 'поиск'} # Create a list with keywords for remove
        filtered_words = [word for word in text.split() if word not in keywords] # Split the text and filter
        prompt = ' '.join(filtered_words) # Create a prompt
        if prompt:  # If something in prompt
            webbrowser.open(f'https://yandex.ru/search/?text={prompt}') # Open browser with prompt
    
    def date_time(self):
        "Method for getting time"
        out = ''
        date = datetime.datetime.now() # Getting date
        time = list(str(date).split()[1]) # create a list for editing time
        for i in range(1,8): # Removing milliseconds
            time.pop(-1)
        out = ''.join(time) # Making string from list
        return out # Return result
    
    def timetable(self):
        "Method for create a school's timetable"
        date = datetime.datetime.today().timetuple() # Get date and time
        table = '' # Out message
        n = 1 # Num of subject
        if date[6] == 6: # if sunday - Weekend. date[6] - day of week
            return 'Выходной'
        if date[3] > 13: # if hour > 13:00 - show table for next day
            table += self.wdays[date[6]+1].capitalize() + '\n' # Create a heading with a day
            for i in self.data[self.wdays[date[6]+1]]: # Create the out message
                table += f'{n}) {i}\n'
                n += 1
            return table # Show timetable
        else:
            table += self.wdays[date[6]].capitalize() + '\n' # Create a heading with a day
            for i in self.data[self.wdays[date[6]]]: # Create the out message for today
                table += f'{n}) {i}\n'
                n += 1
            return table # Show timetable
    
    def load_settings(self):
        "Method for loading settings"
        with open('other/settings.json', encoding='utf-8') as f:
            data = json.load(f)
            return data
    
    def save_settings(self, dataid, datavalue):
        "Method for saving settings"
        with open('other/settings.json', encoding='utf-8') as f:
            data = json.load(f)
        data[dataid] = datavalue
        with open('other/settings.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)