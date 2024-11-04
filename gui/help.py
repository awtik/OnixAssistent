import customtkinter as ctk
def show_help(app):
    "Open settings window"
    # Window Settings
    help_window = ctk.CTkToplevel(app) # Create a TopLevelWindow
    help_window.geometry("400x400") # Set size for this window
    help_window.title("Help") # Set title for window
    help_window.resizable(False, False) # Disable resize function
    help_window.grab_set() # Disable interaction with other windows
    # Creating scrollable frame for settings
    scrollable_frame = ctk.CTkScrollableFrame(help_window, label_text="Help", width=400, height=300)
    scrollable_frame.pack(fill="both", expand=True)
    # Apps label
    apps_label = ctk.CTkLabel(scrollable_frame, text='Приложения', font=('Segoe UI', 18))
    apps_label.pack(pady=5)
    apps_label2 = ctk.CTkLabel(scrollable_frame, text='Перед использованием обязательно\nперенесите ярлыки в папку C:/Onix/apps')
    apps_label2.pack(pady=5)
    # Other help label
    help_label = ctk.CTkLabel(scrollable_frame, text='Если у вас проиходят ошибки, либо есть какие-то вопросы.\ntg: @valerarsdj .')
    help_label.pack(pady=20)