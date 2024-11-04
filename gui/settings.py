import customtkinter as ctk
import os
from modules.addons import Addons
addns = Addons()
# Settings Win
def show_settings(app):
    "Open settings window"
    # Window Settings
    settings_window = ctk.CTkToplevel(app) # Create a TopLevelWindow
    settings_window.geometry("380x250") # Set size for this window
    settings_window.title("Settings") # Set title for window
    settings_window.resizable(False, False) # Disable resize function
    settings_window.grab_set() # Disable interaction with other windows
    # Creating scrollable frame for settings
    scrollable_frame = ctk.CTkScrollableFrame(settings_window, label_text="Settings", width=400, height=300)
    scrollable_frame.pack(fill="both", expand=True)
    # City
    label_city = ctk.CTkLabel(scrollable_frame, text=f"City: {addns.load_settings()['city']}", font=('Segoe UI', 18)) # output the selected city
    label_city.grid(row=0, column=0, sticky='w', padx=5)
    city = ctk.CTkEntry(scrollable_frame, placeholder_text="Enter city", ) # Entry box for choose city
    city.grid(row=1, column=0, sticky='w', padx=5)
    # Widget Groups
    theme_widgets(scrollable_frame) # Theme
    transparency_widgets(scrollable_frame) # Transparency
    color_widgets(scrollable_frame) # Color
    # Save button
    button_save = ctk.CTkButton(scrollable_frame, text="Save", command= lambda: save_settings(settings_window, city, app))
    button_save.grid(pady=40, padx=10, row=7, column=0)
    # Check style
    addns.check_transparency_enable(settings_window) # Adding style for app

def save_settings(win, city, app):
    "Saving settings and destroing window"
    if city.get(): # If something in city entry:
        addns.save_settings('city', city.get().capitalize()) # Saving city in settings.json
    win.destroy() # Destroy settings win
    app.destroy() # Destroy main win
    os.system('python main.py') # Reboot script
    exit()

def theme_widgets(app):
    # Theme label
    theme_label = ctk.CTkLabel(app, text='Choose theme:', font=('Segoe UI', 18)) # Label for themes
    theme_label.grid(padx=5, pady=5, row=0, column=1, sticky='w')
    theme_combobox = ctk.CTkComboBox(app, values=["Light", "Dark"],
                                     command=theme_combobox_call)
    theme_combobox.set(addns.load_settings()['theme'])
    theme_combobox.grid(row=1, column=1)

def transparency_widgets(app):
    transparency_label = ctk.CTkLabel(app, text='Transparency:', font=('Segoe UI', 18))
    transparency_label.grid(padx=5, row=2, column=0, sticky='w')
    transparency_combobox = ctk.CTkComboBox(app, values=["On", "Off"],
                                     command=transparency_combobox_call)
    transparency_combobox.set(addns.load_settings()['transparency'])
    transparency_combobox.grid(padx=5, pady=5, row=3, column=0, sticky='w')
    warning_label = ctk.CTkLabel(app, text='(Windows 10+ | Dark theme only)')
    warning_label.grid(padx=5, row=4, column=0, sticky='w')

def color_widgets(app):
    color_label = ctk.CTkLabel(app, text='Choose color:', font=('Segoe UI', 18)) # Label for themes
    color_label.grid(padx=5, pady=5, row=2, column=1, sticky='w')
    color_combobox = ctk.CTkComboBox(app, values=["Blue", "Green", "Lavender", "Metal"],
                                     command=color_combobox_call)
    color_combobox.set(addns.load_settings()['color'])
    color_combobox.grid(row=3, column=1)

def theme_combobox_call(new_theme):
    addns.save_settings('theme', new_theme) # Saving theme in settings.json

def transparency_combobox_call(transparency_stat):
    addns.save_settings('transparency', transparency_stat) # Saving theme in settings.json

def color_combobox_call(color):
    addns.save_settings('color', color) # Saving color in settings.json