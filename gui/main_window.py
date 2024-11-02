import customtkinter as ctk
from gui.settings import show_settings
from gui.ai_chat import show_ai_chat
from gui.apps import show_apps
import platform, cpuinfo, psutil, wmi
def buttons(app, addns, outlabel, slowly_output):
    "Method for creating buttons on main window"
    # Frame for buttons
    button_frame = ctk.CTkFrame(app) # Create frame
    button_frame.pack(side=ctk.RIGHT, fill=ctk.Y, padx=5, pady=5)
    # Settings button
    settings_button = ctk.CTkButton(button_frame, text="Settings", command=lambda: show_settings(app, addns), corner_radius=20) # Create button
    settings_button.pack(pady=10, padx=10)
    # Chat button
    chat_button = ctk.CTkButton(button_frame, text="Chat with AI", command=lambda: show_ai_chat(app), corner_radius=20) # Create button
    chat_button.pack(pady=10, padx=10)
    # Apps button
    apps_button = ctk.CTkButton(button_frame, text='Apps', command=lambda: show_apps(app, outlabel, slowly_output), corner_radius=20)
    apps_button.pack(pady=10, padx=10)
    # Static weather icon label
    static_weather_icon_label = ctk.CTkLabel(button_frame, text='') # Create icon label
    static_weather_icon_label.pack(side=ctk.BOTTOM)
    addns.weather(addns.load_settings()['city'], static_weather_icon_label)

def pc_details(app, pc_frame_color):
    "Method for creating pc_details frame and working with voice command"
    # Frame
    info_frame = ctk.CTkFrame(app) # Create frame for PC Details and input with output
    info_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=5, pady=5) # Set properties for frame
    # Pc Details frame and label
    for adapter in wmi.WMI().Win32_VideoController(): # Getting gpu model
        gpu = adapter.Name
    # Frame for PC Details
    pc_frame = ctk.CTkFrame(info_frame, corner_radius=10, fg_color=pc_frame_color) # Create a frame
    pc_frame.pack(pady=5)
    # PC Details label
    info_label = ctk.CTkLabel(pc_frame, text=f"OS: {platform.system()} {platform.release()}\n" \
                    f"CPU: {cpuinfo.get_cpu_info()['brand_raw']}\n" \
                    f"GPU: {gpu}\n" \
                    f"RAM: {round(psutil.virtual_memory().total / (1024**3))} ГБ", justify='left', wraplength=400, font=('Segoe UI', 16)) # Create a label with PC Details
    info_label.pack(anchor='w', pady=5, padx=5)
    # User input
    label = ctk.CTkLabel(info_frame, text="Say something...", wraplength=300) # Create label
    label.pack(pady=20)
    # "Вывод" word
    outl = ctk.CTkLabel(info_frame, text='Output: ', wraplength=300, font=('Segoe UI', 16)) # Create label
    outl.pack(pady=5)
    # Output label
    outlabel = ctk.CTkLabel(info_frame, text=' ', wraplength=300, font=('Segoe UI', 16)) # Create label
    outlabel.pack(pady=5)
    # Weather icon label
    weather_icon_label = ctk.CTkLabel(info_frame, text='') # Create icon label
    weather_icon_label.pack()
    return [label, outlabel, weather_icon_label]