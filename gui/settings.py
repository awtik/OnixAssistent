import os
import customtkinter as ctk
import pyaudio
from modules.addons import Addons

addns = Addons()

def show_settings(app):
    settings_window = ctk.CTkToplevel(app)
    settings_window.geometry("450x300")
    settings_window.title("Settings")
    settings_window.resizable(False, False)
    settings_window.grab_set()

    scrollable_frame = ctk.CTkScrollableFrame(settings_window, label_text="Settings", width=400, height=300)
    scrollable_frame.pack(fill="both", expand=True)

    try:
        city_name = addns.load_settings().get('city', '')  # Safely get city name
        label_city = ctk.CTkLabel(scrollable_frame, text=f"City: {city_name}", font=('Segoe UI', 18))
        label_city.grid(row=0, column=0, sticky='w', padx=5)
    except Exception as e:
        print(f"Error loading settings: {e}")
        label_city = ctk.CTkLabel(scrollable_frame, text="City: Unknown", font=('Segoe UI', 18))
        label_city.grid(row=0, column=0, sticky='w', padx=5)

    city_entry = ctk.CTkEntry(scrollable_frame, placeholder_text="Enter city")
    city_entry.grid(row=1, column=0, sticky='w', padx=5)

    theme_widgets(scrollable_frame)
    transparency_widgets(scrollable_frame)
    color_widgets(scrollable_frame)
    device_selection_widgets(scrollable_frame)
    tts_congifure_widgets(scrollable_frame)

    button_save = ctk.CTkButton(scrollable_frame, text="Save", command=lambda: save_settings(settings_window, city_entry, app))
    button_save.grid(pady=40, padx=10, row=9, column=0)

    addns.check_transparency_enable(settings_window)

def save_settings(win, city_entry, app):
    """Save settings and reboot"""
    
    city_value = city_entry.get().capitalize()
    if city_value:  # If city entry is not empty
        addns.save_settings('city', city_value)
        
    win.destroy()
    app.destroy()
    os.system('python main.pyw')  # Restart script
    exit()

def theme_widgets(root):
    """Create theme selection widgets."""
    
    theme_label = ctk.CTkLabel(root, text='Choose theme:', font=('Segoe UI', 18))
    theme_label.grid(padx=5, pady=5, row=0, column=1, sticky='w')

    theme_combobox = ctk.CTkComboBox(root, values=["Light", "Dark"], command=theme_combobox_call, state='readonly')
    theme_combobox.set(addns.load_settings().get('theme', 'Light'))  # Default to 'Light'
    theme_combobox.grid(row=1, column=1, sticky='w')

def transparency_widgets(root):
    """Create transparency selection widgets."""
    
    transparency_label = ctk.CTkLabel(root, text='Transparency:', font=('Segoe UI', 18))
    transparency_label.grid(padx=5, row=2, column=0, sticky='w')

    transparency_combobox = ctk.CTkComboBox(root, values=["On", "Off"], command=transparency_combobox_call, state='readonly')
    transparency_combobox.set(addns.load_settings().get('transparency', 'Off'))  # Default to 'Off'
    transparency_combobox.grid(padx=5, pady=5, row=3, column=0, sticky='w')

    warning_label = ctk.CTkLabel(root, text='(Windows 11 | Dark theme only)')
    warning_label.grid(padx=5, row=4, column=0, sticky='w')

def color_widgets(root):
    """Create color selection widgets."""
    
    color_label = ctk.CTkLabel(root, text='Choose color:', font=('Segoe UI', 18))
    color_label.grid(padx=5, pady=5, row=2, column=1, sticky='w')

    color_combobox = ctk.CTkComboBox(root, values=["Blue", "Green", "Lavender", "Metal", "Rime"], command=color_combobox_call, state='readonly')
    color_combobox.set(addns.load_settings().get('color', 'Blue'))  # Default to 'Blue'
    color_combobox.grid(row=3, column=1, sticky='w')

def device_selection_widgets(root):
    """Creating widgets for device selection"""
    
    input_devices, output_devices = addns.get_audio_devices()
    
    input_device_label = ctk.CTkLabel(root, text='Select Input Device:', font=('Segoe UI', 18))
    input_device_label.grid(row=5, column=0, sticky='w', padx=5)
    
    input_device_values = [(ind, name) for ind, name in input_devices]
    input_device_combobox = ctk.CTkComboBox(
        root, values=[name for ind, name in input_devices], command=lambda x: save_input_device(input_device_values, x), state='readonly', width=200
    )
    input_device_name = pyaudio.PyAudio().get_device_info_by_index(addns.load_settings().get('input_device')).get('name')
    input_device_combobox.set(input_device_name)
    input_device_combobox.grid(row=6, column=0, sticky='w', padx=5)
    
    output_device_label = ctk.CTkLabel(root, text='Select Output Device:', font=('Segoe UI', 18))
    output_device_label.grid(row=5, column=1, sticky='w', padx=5)
    
    output_device_values = [(ind, name) for ind, name in output_devices]
    output_device_combobox = ctk.CTkComboBox(
        root, values=[name for ind, name in output_devices], command=lambda x: save_output_device(output_device_values, x), state='readonly', width=200
    )
    output_device_name = pyaudio.PyAudio().get_device_info_by_index(addns.load_settings().get('output_device')).get('name')
    output_device_combobox.set(addns.decode_device_name(output_device_name))
    output_device_combobox.grid(row=6, column=1, sticky='w', padx=5)

def tts_congifure_widgets(root,):
    tts_configure_label = ctk.CTkLabel(root, text='TTS:', font=('Segoe UI', 18))
    tts_configure_label.grid(row=7, column=0, sticky='w', padx=5, pady=5)
    tts_combobox = ctk.CTkComboBox(
        root, values=['On', 'Off'], command=lambda event: tts_configure_call(event), state='readonly'
    )
    tts_combobox.set(addns.load_settings()['tts'])
    tts_combobox.grid(row=8, column=0, sticky='w', padx=5)

def theme_combobox_call(new_theme):
    addns.save_settings('theme', new_theme)

def transparency_combobox_call(transparency_state):
    addns.save_settings('transparency', transparency_state)

def color_combobox_call(color):
    addns.save_settings('color', color)

def save_input_device(input_device_values, selected_name):
    """Save the selected input device."""
    selected_device = next((ind for ind, name in input_device_values if name == selected_name), None)
    if selected_device is not None:
        addns.save_settings('input_device', selected_device)

def save_output_device(output_device_values, selected_name):
    """Save the selected output device."""
    selected_device = next((ind for ind, name in output_device_values if name == selected_name), None)
    if selected_device is not None:
        addns.save_settings('output_device', selected_device)

def tts_configure_call(tts):
    addns.save_settings('tts', tts)