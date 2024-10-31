import os
import json

def get_apps(apps_folder='C:/Onix/apps'):
    "Getting all app names"
    return [os.path.splitext(app)[0] for app in os.listdir(apps_folder)] # Return list with all apps in folder

def load_keywords(outlabel, slowly_output, file_path='other/apps.json'):
    "Getting all keywords for apps from json"
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0: # If apps.json in folder:
        with open(file_path, 'r') as file: # Open apps.json
            try:
                return json.load(file) # Return dict with apps and their keywords
            except json.JSONDecodeError: # If error:
                slowly_output("Ошибка: Невозможно декодировать JSON. Файл поврежден.", outlabel) # Return error message and empty dict
                return {}
    return {}

def save_keywords(keywords, file_path='other/apps.json'):
    "Saving keywords for app in json file"
    with open(file_path, 'w') as file: # Open json file
        json.dump(keywords, file, indent=4) # Save words in json

def open_app_by_keyword(command, outlabel, slowly_output, apps_folder='C:/Onix/apps'):
    "Open app by keyword"
    keyword = command.replace("оникс открой ", "").strip() # Get keword from command
    keywords = load_keywords() # Loading keywords
    # Searching app by keyword
    for app_name, app_keywords in keywords.items():
        if keyword.lower() in app_keywords.lower():  # Lowercase comparison
            app_path = os.path.join(apps_folder, f"{app_name}.lnk") # Creating path for app
            if os.path.exists(app_path): # If app in folder:
                os.startfile(app_path) # Open app
                slowly_output(f"Запускаю приложение: {app_name}", outlabel)
                return
            else:
                slowly_output(f"Файл приложения {app_name} не найден в папке {apps_folder}.", outlabel)
                return
    slowly_output(f"Приложение с ключевым словом '{keyword}' не найдено.", outlabel)