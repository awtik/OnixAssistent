import customtkinter as ctk
from tkinter import filedialog
from modules.apps import save_keywords, load_keywords
from modules.addons import Addons

addons = Addons()

def show_apps(main_app, outlabel, slowly_output):
    settings_window = ctk.CTkToplevel(main_app)
    settings_window.geometry("500x400")
    settings_window.title("Настройки")
    settings_window.resizable(False, False)
    settings_window.grab_set()

    apps_frame = ctk.CTkScrollableFrame(settings_window, label_text="Apps", width=500, height=350)
    apps_frame.pack(fill="both", expand=True)

    path_label = ctk.CTkLabel(apps_frame, text="Path")
    path_label.grid(row=0, column=0, pady=5, padx=10)

    keywords_label = ctk.CTkLabel(apps_frame, text="Keyword")
    keywords_label.grid(row=0, column=1, pady=5, padx=10)

    keywords = load_keywords(outlabel, slowly_output)
    path_entries = {}
    keyword_entries = {}

    def add_app_row(app_name=None, app_path=""):
        index = len(path_entries) + 1
        app_name = app_name or f"app_{index}"

        path_entry = ctk.CTkEntry(apps_frame, width=230)
        path_entry.grid(row=index, column=0, padx=10, pady=5)
        path_entry.insert(0, app_path)
        path_entries[app_name] = path_entry

        def choose_path():
            app_path = filedialog.askopenfilename(title=f"Выберите файл для {app_name}")
            if app_path:
                path_entries[app_name].delete(0, ctk.END)
                path_entries[app_name].insert(0, app_path)
                add_app_row()

        choose_path_button = ctk.CTkButton(apps_frame, text="...", command=choose_path, width=30)
        choose_path_button.grid(row=index, column=0, padx=10, sticky='e')

        keyword_entry = ctk.CTkEntry(apps_frame, width=100)
        keyword_entry.grid(row=index, column=1, padx=10, pady=5)
        keyword_entry.insert(0, keywords.get(app_name, {}).get("keyword", ""))
        keyword_entries[app_name] = keyword_entry

    for app_name, data in keywords.items():
        add_app_row(app_name=app_name, app_path=data.get("path", ""))
    add_app_row()

    def save_settings():
        new_keywords = {}
        for app_name, path_entry in path_entries.items():
            path = path_entry.get().strip()
            keyword = keyword_entries[app_name].get().strip()
            if path and keyword:
                new_keywords[app_name] = {"path": path, "keyword": keyword}
        save_keywords(new_keywords)
        settings_window.destroy()

    save_button = ctk.CTkButton(apps_frame, text="Save", command=save_settings)
    save_button.grid(row=len(path_entries) + 15, column=0, pady=20)

    addons.check_transparency_enable(settings_window)