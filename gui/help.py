import customtkinter as ctk
from modules.addons import Addons

addons = Addons()

def show_help(main_app):
    """Open help window with usage information."""
    
    help_window = ctk.CTkToplevel(main_app)
    help_window.geometry("400x400")
    help_window.title("Help")
    help_window.resizable(False, False)
    help_window.grab_set()

    help_frame = ctk.CTkScrollableFrame(help_window, label_text="Help", width=400, height=300)
    help_frame.pack(fill="both", expand=True)

    help_label = ctk.CTkLabel(
        help_frame,
        text="Если у вас происходят ошибки, либо есть вопросы.\nTelegram: @valerarsdj"
    )
    help_label.pack(pady=20)

    addons.check_transparency_enable(help_window)