import customtkinter as ctk
from modules.apps import get_apps, save_keywords, load_keywords
from tkinter import Canvas, Scrollbar

# Окно приложений
def show_apps(app, outlabel, slowly_output):
    "Открыть окно приложений"
    # Настройки окна
    apps_window = ctk.CTkToplevel(app)  # Создаем окно TopLevel
    apps_window.geometry("450x350")  # Задаем размер окна
    apps_window.title("Настройки")  # Заголовок окна
    apps_window.resizable(False, False)  # Запрещаем изменение размера
    apps_window.grab_set()  # Отключаем взаимодействие с другими окнами

    # Устанавливаем цвет фона
    bg_color = apps_window.cget("bg")  # Получаем цвет фона от главного окна

    # Создаем холст с полосой прокрутки
    canvas = Canvas(apps_window, bg=bg_color, highlightthickness=0)  # Убираем границу и задаем цвет фона
    canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    
    scrollbar = Scrollbar(apps_window, orient="vertical", command=canvas.yview, bg=bg_color)
    scrollbar.pack(side=ctk.RIGHT, fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Фрейм внутри холста для виджетов
    apps_frame = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=apps_frame, anchor="nw")
    # Функция настройки области прокрутки
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    apps_frame.bind("<Configure>", on_frame_configure)

    apps_label = ctk.CTkLabel(apps_frame, text='App:')
    apps_label.grid(row=0, column=0, pady=5)
    keywords_label = ctk.CTkLabel(apps_frame, text='Keyword:')
    keywords_label.grid(row=0, column=1, pady=5)

    # Загружаем приложения и ключевые слова
    apps = get_apps()
    keywords = load_keywords(outlabel, slowly_output)
    # Словарь для хранения виджетов ввода
    rename_entries = {}
    # Отображение имен приложений и полей для ввода ключевых слов
    for index, app_name in enumerate(apps):
        index += 1
        # Метка с именем приложения
        label = ctk.CTkLabel(apps_frame, text=f"Приложение: {app_name}")
        label.grid(row=index, column=0, padx=10, pady=5, sticky="w")
        
        # Поле для ввода ключевых слов
        entry = ctk.CTkEntry(apps_frame, width=200)
        entry.grid(row=index, column=1, padx=10, pady=5)
        entry.insert(0, keywords.get(app_name, ""))  # Предзаполнение ключевых слов, если они есть
        rename_entries[app_name] = entry

    # Функция для сохранения настроек
    def save_settings():
        new_keywords = {app_name: entry.get() for app_name, entry in rename_entries.items()}
        save_keywords(new_keywords)  # Сохранение ключевых слов в apps.json
        apps_window.destroy()  # Закрытие окна настроек

    # Кнопка "Сохранить"
    button_save = ctk.CTkButton(apps_frame, text="Сохранить", command=save_settings)
    button_save.grid(row=len(apps)+1, column=1, pady=20)