import customtkinter as ctk
from gui.settings import show_settings
from gui.ai_chat import show_ai_chat
from gui.apps import show_apps
from gui.help import show_help
import platform
import cpuinfo
import psutil
import wmi

def create_main_buttons(main_app, addons, output_label, slow_output):
    """Create and configure main buttons on the application window."""
    
    button_frame = ctk.CTkFrame(main_app)
    button_frame.pack(side=ctk.RIGHT, fill=ctk.Y, padx=5, pady=5)

    settings_button = ctk.CTkButton(
        button_frame, text="Settings", command=lambda: show_settings(main_app), corner_radius=20
    )
    settings_button.pack(pady=10, padx=10)

    ai_chat_button = ctk.CTkButton(
        button_frame, text="Chat with AI", command=lambda: show_ai_chat(main_app), corner_radius=20
    )
    ai_chat_button.pack(pady=10, padx=10)

    apps_button = ctk.CTkButton(
        button_frame, text="Apps", command=lambda: show_apps(main_app, output_label, slow_output), corner_radius=20
    )
    apps_button.pack(pady=10, padx=10)

    help_button = ctk.CTkButton(
        button_frame, text="Help", command=lambda: show_help(main_app), corner_radius=20
    )
    help_button.pack(pady=10, padx=10)

    temp_label = ctk.CTkLabel(button_frame, text='', font=("Arial", 20))
    temp_label.pack(side=ctk.BOTTOM, pady=10)
    weather_icon_label = ctk.CTkLabel(button_frame, text='')
    weather_icon_label.pack(side=ctk.BOTTOM, anchor='s')
    addons.weather_right_data(addons.load_settings()['city'], weather_icon_label, temp_label)


def display_pc_details(main_app, frame_color):
    """Create a frame to display PC details and initialize labels for voice command interaction."""
    
    pc_info_frame = ctk.CTkFrame(main_app)
    pc_info_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=5, pady=5)

    try:
        for adapter in wmi.WMI().Win32_VideoController():
            gpu_model = adapter.Name
    except Exception as e:
        gpu_model = "Unknown GPU"
        print(f"Error retrieving GPU info: {e}")

    pc_details_frame = ctk.CTkFrame(pc_info_frame, corner_radius=10, fg_color=frame_color)
    pc_details_frame.pack(pady=5)

    system_info_label = ctk.CTkLabel(
        pc_details_frame,
        text=f"OS: {platform.system()} {platform.release()}\n"
             f"CPU: {cpuinfo.get_cpu_info()['brand_raw']}\n"
             f"GPU: {gpu_model}\n"
             f"RAM: {round(psutil.virtual_memory().total / (1024**3))} ГБ",
        justify='left', wraplength=400, font=('Segoe UI', 16)
    )
    system_info_label.pack(anchor='w', pady=5, padx=5)

    prompt_label = ctk.CTkLabel(pc_info_frame, text="Say something...", wraplength=300)
    prompt_label.pack(pady=20)

    output_prefix_label = ctk.CTkLabel(pc_info_frame, text="Output:", wraplength=300, font=('Segoe UI', 16))
    output_prefix_label.pack(pady=5)

    output_label = ctk.CTkLabel(pc_info_frame, text='', wraplength=300, font=('Segoe UI', 16))
    output_label.pack(pady=5)

    weather_icon_label = ctk.CTkLabel(pc_info_frame, text='')
    weather_icon_label.pack()

    return [prompt_label, output_label, weather_icon_label]