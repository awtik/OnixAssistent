import customtkinter as ctk
import os
# Settings Win
def show_settings(app, addns):
    "Open settings window"
    # Window Settings
    settings_window = ctk.CTkToplevel(app) # Create a TopLevelWindow
    settings_window.geometry("225x225") # Set size for this window
    settings_window.title("Settings") # Set title for window
    settings_window.resizable(False, False) # Disable resize function
    settings_window.grab_set() # Disable interaction with other windows
    # Settings1 frame
    settings_frame = ctk.CTkFrame(settings_window) # Create frame for widgets
    settings_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=0, pady=0)
    # City
    label_city = ctk.CTkLabel(settings_frame, text=f"City: {addns.load_settings()['city']}", font=('Segoe UI', 18)) # output the selected city
    label_city.pack(anchor='w', padx=5)
    city = ctk.CTkEntry(settings_frame, placeholder_text="Enter city", ) # Entry box for choose city
    city.pack(anchor='w', padx=5)
    # Theme
    choose_theme = ctk.StringVar(value=addns.load_settings()['theme']) # variable for theme
    # Theme label
    theme_label = ctk.CTkLabel(settings_frame, text='Choose theme:', font=('Segoe UI', 18)) # Label for themes
    theme_label.pack(anchor='w', padx=5, pady=5)
    light_theme_button = ctk.CTkRadioButton(settings_frame, text='Light', variable=choose_theme, value='Light', border_width_unchecked=3,
                                            border_width_checked=4, ) # Create a radio button for choosing light theme
    light_theme_button.pack(anchor='w', padx=5, pady=7)
    dark_theme_button = ctk.CTkRadioButton(settings_frame, text='Dark', variable=choose_theme, value='Dark', border_width_unchecked=3,
                                           border_width_checked=4) # Create a radio button for choosing dark theme
    dark_theme_button.pack(anchor='w', padx=5, pady=3)
    # Save button
    button_save = ctk.CTkButton(settings_frame, text="Сохранить", command= lambda: save_settings(settings_window, city, choose_theme.get(), app, addns))
    button_save.pack(pady=20)

def save_settings(win, city, new_theme, app, addns):
    "Saving settings and destroing window"
    if city.get(): # If something in city entry:
        addns.save_settings('city', city.get().capitalize()) # Saving city in settings.json
    addns.save_settings('theme', new_theme) # Saving theme in settings.json
    win.destroy() # Destroy settings win
    app.destroy() # Destroy main win
    os.system('python main.py') # Reboot script
    exit()