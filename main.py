from modules.recognizeClass import Recognize
from modules.commands import Commands
from modules.addons import Addons
import customtkinter as ctk
import threading
from gui.main_window import buttons, pc_details

cmnds, r, addns = Commands(), Recognize(), Addons() # Initialization Classes

###################################################################################################
# Main window Settings
theme = addns.load_settings()['theme'] # Getting theme from settings
ctk.set_appearance_mode(theme) # Set theme from settings
ctk.set_default_color_theme("blue") # Set color for app
app = ctk.CTk() # Create main window
app.title("Onix") # Set title
app.geometry("600x400") # Set size for app
app.resizable(False, False) # Disable resize function
# Set frame's color
if theme == 'Light': pc_frame_color='#c6c6c6' # Set color for PC Details frame
else: pc_frame_color='#232323'
###################################################################################################
widgets = pc_details(app, pc_frame_color)
label = widgets[0]
outlabel = widgets[1]
weather_icon_label = widgets[2]
###################################################################################################
buttons(app, addns, outlabel, cmnds.slowly_output)
###################################################################################################
# Запускаем распознавание речи в отдельном потоке
recognition_thread = threading.Thread(target=r.recognize_speech, args=(label, cmnds, outlabel, app, cmnds.slowly_output, weather_icon_label), daemon=True)
recognition_thread.start() # Start recognition

app.mainloop()