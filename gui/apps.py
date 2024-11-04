import customtkinter as ctk
from modules.apps import get_apps, save_keywords, load_keywords
from modules.addons import Addons
addns = Addons()
# Apps window
def show_apps(app, outlabel, slowly_output):
    "Showing apps window"
    # Window settings
    apps_window = ctk.CTkToplevel(app)  # Creating TopLevel window
    apps_window.geometry("400x350")  # Setting window size
    apps_window.title("Настройки")  # Setting window title
    apps_window.resizable(False, False) # Disable resize function
    apps_window.grab_set()  # Disable interaction with other windows

    # Creating scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(apps_window, label_text="Apps", width=400, height=300)
    scrollable_frame.pack(fill="both", expand=True)

    # Labels for columns
    apps_label = ctk.CTkLabel(scrollable_frame, text='App')
    apps_label.grid(row=0, column=0, pady=5, padx=10)
    keywords_label = ctk.CTkLabel(scrollable_frame, text='Keyword')
    keywords_label.grid(row=0, column=1, pady=5, padx=10)

    # Loading apps and keywords
    apps = get_apps()
    keywords = load_keywords(outlabel, slowly_output)

    rename_entries = {} # Widgets dict

    # Showing labels and entries
    for index, app_name in enumerate(apps, start=1):
        # Label with app name
        label = ctk.CTkLabel(scrollable_frame, text=app_name)
        label.grid(row=index, column=0, padx=10, pady=5, sticky="w")
        
        # Entry case for keywords
        entry = ctk.CTkEntry(scrollable_frame, width=200)
        entry.grid(row=index, column=1, padx=10, pady=5)
        entry.insert(0, keywords.get(app_name, ""))  # Insert keywords if it in apps.json
        rename_entries[app_name] = entry

    def save_settings():
        "Saving keywords"
        new_keywords = {app_name: entry.get() for app_name, entry in rename_entries.items()}
        save_keywords(new_keywords)  # Saving keywords
        apps_window.destroy()  # Close window

    # Save button
    button_save = ctk.CTkButton(scrollable_frame, text="Save", command=save_settings)
    button_save.grid(row=len(apps) + 1, column=0, pady=20)
    addns.check_transparency_enable(apps_window) # Adding style for app