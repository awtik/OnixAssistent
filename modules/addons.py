import json
import os
import datetime
import requests
import webbrowser
import pyaudio
from io import BytesIO
from PIL import Image, ImageTk
from customtkinter import CTkImage
from translate import Translator
import pywinstyles as pws

class Addons:
    def __init__(self):
        """Initialize the Addons class with API key and translator."""
        self.api_key = "0cef33e68245bf3fa8bf5147a6a330ea"
        self.translator = Translator(to_lang="ru")
        self.weekdays = {
            0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
            5: 'saturday',
            6: 'sunday'
        }
        self.data = self.load_settings()

    def load_settings(self):
        """Load settings from a JSON file."""
        try:
            with open(f'{os.curdir}/other/settings.json', encoding='utf-8') as f:
                return json.load(f)
        except:
            with open(f'{os.curdir}/other/settings.json', 'w'):
                    pass

    def save_settings(self, key, value):
        """Save a specific setting in the settings JSON file."""
        self.data[key] = value
        with open(f'{os.curdir}/other/settings.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def weather_output(self, city, icon_label):
        """Get weather data for a specified city and update the icon label."""
        url = f"http://ru.api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()

            weather = {
                "city": weather_data["name"],
                "temperature": weather_data["main"]["temp"],
                "description": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "wind_speed": weather_data["wind"]["speed"],
                "icon": weather_data["weather"][0]["icon"]
            }

            icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
            img_data = requests.get(icon_url).content
            img = Image.open(BytesIO(img_data))
            img = CTkImage(img, size=(80, 80))

            icon_label.configure(image=img)
            icon_label.image = img

            return f'В городе {self.translator.translate(weather["city"])} сейчас \n' \
                   f'{self.translator.translate(weather["description"]).capitalize()}, ' \
                   f'{round(weather["temperature"])}° | {weather["description"]}'
        except requests.exceptions.RequestException as e:
            return f"Ошибка при получении данных о погоде: {e}"
    
    def weather_right_data(self, city, icon_label, temp_label):
        URL = f"http://ru.api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(URL)
            data = response.json()
            if response.status_code == 200:
                weather = {
                    "city": data["name"],
                    "temp": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"]
                }
                icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
                icon_response = requests.get(icon_url)
                icon_image = Image.open(BytesIO(icon_response.content))
                icon_image = icon_image.resize((100, 100))
                icon_photo = ImageTk.PhotoImage(icon_image)
                icon_label.configure(image=icon_photo)
                icon_label.image = icon_photo
                temp_label.configure(text=f"{round(weather['temp'])}°C")
            
        except Exception as e:
            print("Не удалось получить данные:", e)
            return None

    def search(self, text, launch_word):
        """Search for a query in the web browser, filtering out unnecessary keywords."""
        keywords = {launch_word, 'найди', 'найти', 'привет', 'поиск'}
        filtered_words = [word for word in text.split() if word not in keywords]
        prompt = ' '.join(filtered_words).strip()
        if prompt:
            webbrowser.open(f'https://yandex.ru/search/?text={prompt}')

    def time(self):
        """Return the current time as a string."""
        return datetime.datetime.now().strftime("%H:%M:%S")

    def timetable(self):
        """Create a school timetable based on the current day and time."""
        current_date = datetime.datetime.today()
        day_index = current_date.weekday()
        if day_index == 6:  # Sunday
            return 'Выходной'

        # Adjust day index for the timetable
        if current_date.hour > 13:
            day_index = (day_index + 1) % 7  # Next day

        timetable_msg = f"{self.weekdays[day_index].capitalize()}\n"
        subjects = self.data[self.weekdays[day_index]]

        for i, subject in enumerate(subjects, start=1):
            timetable_msg += f'{i}) {subject}\n'
        return timetable_msg

    def check_transparency_enable(self, app):
        """Apply style to the app based on transparency and theme settings."""
        settings = self.load_settings()
        if settings['transparency'] == 'On':
            if settings['theme'] == 'Dark':
                pws.apply_style(app, 'acrylic')
            elif settings['theme'] == 'Light':
                self.save_settings('transparency', 'Off')

    def decode_device_name(self, name):
        try:
            return name.encode('WINDOWS-1251').decode('utf-8')
        except Exception as e:
            print(f"Ошибка при декодировании имени устройства: {e}")
            return name
    
    def get_audio_devices(self):
        """Getting list of user's audio devices"""
        p = pyaudio.PyAudio()
        input_devices = []
        output_devices = []
        host_api_count = p.get_host_api_count()
        for api_index in range(host_api_count):
            # Получаем информацию о хост API
            host_api_info = p.get_host_api_info_by_index(api_index)
            api_name = host_api_info['name']

            # Фильтруем только необходимые API
            if api_name not in ["MME"]:
                continue

            # Получаем количество устройств в этом API
            device_count = host_api_info['deviceCount']
            for device_index in range(device_count):
                # Получаем информацию о конкретном устройстве по индексу API хоста
                device_info = p.get_device_info_by_host_api_device_index(api_index, device_index)
                if device_info['maxInputChannels'] > 0:
                    input_devices.append((device_info['index'], self.decode_device_name(device_info['name'])))
                if device_info['maxOutputChannels'] > 0:
                    output_devices.append((device_info['index'], self.decode_device_name(device_info['name'])))

        p.terminate()

        return input_devices, output_devices