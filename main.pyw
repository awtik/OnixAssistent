from modules.recognize_class import Recognize
import threading
import os
import customtkinter as ctk
from modules.commands import Commands
from modules.addons import Addons
from gui.main_window import create_main_buttons, display_pc_details

cmnds = Commands()
r = Recognize()
addns = Addons()

settings = addns.load_settings()
theme = settings.get('theme', 'Light')
color = settings.get('color', 'default')

ctk.set_appearance_mode(theme)
ctk.set_default_color_theme(f'{os.curdir}/colors/{color}.json')

app = ctk.CTk()
app.title("Onix")
app.geometry("600x400")
app.resizable(False, False)

pc_frame_color = '#c6c6c6' if theme == 'Light' else '#232323'

widgets = display_pc_details(app, pc_frame_color)
label, outlabel, weather_icon_label = widgets

create_main_buttons(app, addns, outlabel, cmnds.slowly_output)

def run_recognition():
    try:
        r.recognize_speech(label, cmnds, outlabel, app, cmnds.slowly_output, weather_icon_label)
    except Exception as e:
        print(f"Ошибка в потоке распознавания: {e}")

recognition_thread = threading.Thread(target=run_recognition, daemon=True)
recognition_thread.start()

addns.check_transparency_enable(app)
app.mainloop()