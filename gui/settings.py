import customtkinter as ctk
import os
# Settings Win
def show_settings(app, addns):
    "Open settings window"
    # Window Settings
    settings_window = ctk.CTkToplevel(app) # Create a TopLevelWindow
    settings_window.geometry("350x250") # Set size for this window
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
    # Theme
    choose_theme = ctk.StringVar(value=addns.load_settings()['theme']) # variable for theme
    # Theme label
    theme_label = ctk.CTkLabel(scrollable_frame, text='Choose theme:', font=('Segoe UI', 18)) # Label for themes
    theme_label.grid(padx=5, pady=5, row=0, column=1, sticky='w')
    light_theme_button = ctk.CTkRadioButton(scrollable_frame, text='Light', variable=choose_theme, value='Light', border_width_unchecked=3,
                                            border_width_checked=4, ) # Create a radio button for choosing light theme
    light_theme_button.grid(padx=5, pady=7, row=1, column=1, sticky='w')
    dark_theme_button = ctk.CTkRadioButton(scrollable_frame, text='Dark', variable=choose_theme, value='Dark', border_width_unchecked=3,
                                           border_width_checked=4) # Create a radio button for choosing dark theme
    dark_theme_button.grid(padx=5, pady=3, row=2, column=1, sticky='w')
    # Save button
    button_save = ctk.CTkButton(scrollable_frame, text="Save", command= lambda: save_settings(settings_window, city, choose_theme.get(), app, addns))
    button_save.grid(pady=40, padx=10, row=4, column=0)

def save_settings(win, city, new_theme, app, addns):
    "Saving settings and destroing window"
    if city.get(): # If something in city entry:
        addns.save_settings('city', city.get().capitalize()) # Saving city in settings.json
    addns.save_settings('theme', new_theme) # Saving theme in settings.json
    win.destroy() # Destroy settings win
    app.destroy() # Destroy main win
    os.system('python main.py') # Reboot script
    exit()