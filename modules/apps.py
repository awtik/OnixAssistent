import os
import json
import shutil
from tkinter import filedialog, Tk

def load_keywords(outlabel, slowly_output, file_path='C:/Onix/apps.json'):
    if not os.path.exists(file_path):
        source_path = os.path.join(os.path.abspath(os.curdir), 'other', 'apps.json')
        shutil.copy(source_path, 'C:/Onix/')

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                slowly_output("Ошибка: Невозможно декодировать JSON. Файл поврежден.", outlabel)
                return {}
    return {}

def save_keywords(keywords, file_path='C:/Onix/apps.json'):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(keywords, file, ensure_ascii=False, indent=4)

def set_keyword_for_app(outlabel, slowly_output, keyword, file_path='C:/Onix/apps.json'):
    if not keyword.strip():
        slowly_output("Ключевое слово не может быть пустым.", outlabel)
        return

    keywords = load_keywords(outlabel, slowly_output, file_path)
    Tk().withdraw()  
    app_path = filedialog.askopenfilename(title="Выберите файл приложения для запуска")
    
    if app_path:
        app_name = f"app_{len(keywords) + 1}"
        keywords[app_name] = {'path': app_path, 'keyword': keyword}
        save_keywords(keywords, file_path)
        slowly_output(f"Приложение '{app_name}' сохранено с ключевым словом '{keyword}'.", outlabel)
    else:
        slowly_output("Файл не был выбран.", outlabel)

def open_app_by_keyword(command, outlabel, slowly_output, file_path='C:/Onix/apps.json'):
    keyword = command.replace("оникс открой ", "").strip().lower()
    keywords = load_keywords(outlabel, slowly_output, file_path)

    for app_name, app_info in keywords.items():
        if keyword == app_info['keyword'].lower():
            app_path = app_info['path']
            if os.path.exists(app_path):
                os.startfile(app_path)
                return f"Запускаю приложение: {app_info['keyword']}"

            return f"Файл приложения '{app_info['keyword']}' не найден по пути '{app_path}'."

    return f"Приложение с ключевым словом '{keyword}' не найдено."