from modules.recognizeClass import Recognize
from modules.commands import Commands
from modules.addons import Addons
from modules.gptResponse import get_answer
import customtkinter as ctk
import platform, cpuinfo, psutil, threading, wmi, os, asyncio

cmnds, r, addns = Commands(), Recognize(), Addons() # Initialization Classes
#####################################################################################################################
# App GUI
# Settings Win
def show_settings():
    "Open settings window"
    # Window Settings
    settings_window = ctk.CTkToplevel(app) # Create a TopLevelWindow
    settings_window.geometry("350x300") # Set size for this window
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
    button_save = ctk.CTkButton(settings_frame, text="Сохранить", command= lambda: save_settings(settings_window, city, choose_theme.get()))
    button_save.pack(pady=20)

def save_settings(win, city, new_theme):
    "Saving settings and destroing window"
    if city.get(): # If something in city entry:
        addns.save_settings('city', city.get().capitalize()) # Saving city in settings.json
    addns.save_settings('theme', new_theme) # Saving theme in settings.json
    win.destroy() # Destroy settings win
    app.destroy() # Destroy main win
    os.system('python gui.py') # Reboot script
    exit()

###################################################################################################
# AI chat window
def show_ai_chat():
    "Open AI chat window"
    # Window Settings
    ai_window = ctk.CTkToplevel(app) # Create Toplevel window for AI chat
    ai_window.geometry("450x350") # Set size for AI chat
    ai_window.title("AI Chat") # Set title
    ai_window.resizable(False, False) # Disable resize function
    ai_window.grab_set() # Disable interaction with other windows
    # Textbox for chat
    response_text = ctk.CTkTextbox(ai_window, wrap='word', width=400, height=250) # Create a textbox and set size
    response_text.pack(padx=10, pady=10)
    response_text.configure(state="disabled") # Disable interacting with textbox
    # Prompt Entrybox
    entry = ctk.CTkEntry(ai_window, width=350) # Create entry
    entry.pack(padx=10, pady=(0, 10))
    entry.bind('<Return>', lambda event: asyncio.run(send_message(entry, response_text, ai_window))) # IF keydown Enter - start send_message
    # Clear Chat button
    clear_button = ctk.CTkButton(ai_window, text="Очистить чат", command=lambda: clear_chat(response_text)) # Create button for clear chat
    clear_button.pack(pady=5)

async def type_text(widget, text, delay=0.001):
    "Function for slowing print the text in AI Chat"
    for char in text:
        widget.insert('end', char) # Insert char into textbox
        widget.update() # Update textbox
        widget.see('end') # automatic scrolling to the end
        await asyncio.sleep(delay) # Delay

async def send_message(entry, response_text, app):
    "function for send_message in AI chat"
    prompt = entry.get() # Get prompt from entry
    if prompt.lower() == 'stop chat': # Stop chatting
        app.destroy() # Quit from AI chat
        return

    entry.delete(0, 'end') # Clear entry box
    response_text.configure(state="normal") # Set normal state for textbox
    response_text.insert('end', f"Вы: {prompt}\n") # Insert user msg into textbox
    response_text.see('end') # automatic scrolling to the end

    response = await get_answer(prompt) # Get answer from AI
    await type_text(response_text, response, delay=0.02) # Slowing print AI's answer
    print('')
    response_text.configure(state="disabled") # Disable interacting with textbox again
def clear_chat(textbox):
    "Function for clear AI chat"
    textbox.configure(state='normal')
    textbox.delete("1.0", 'end')
    textbox.configure(state="disabled") # Disable interacting with textbox again

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
# PC Details and work with commands
# Frame
info_frame = ctk.CTkFrame(app) # Create frame for PC Details and input with output
info_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=0, pady=0) # Set properties for frame
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
###################################################################################################
# Buttons
# Frame for buttons
button_frame = ctk.CTkFrame(app) # Create frame
button_frame.pack(side=ctk.RIGHT, fill=ctk.Y, padx=10, pady=0)
# Settings button
settings_button = ctk.CTkButton(button_frame, text="Settings", command=show_settings, corner_radius=20) # Create button
settings_button.pack(pady=10, padx=10)
# Chat button
chat_button = ctk.CTkButton(button_frame, text="Chat with AI", command=show_ai_chat, corner_radius=20) # Create button
chat_button.pack(pady=10, padx=10)
# Static weather icon label
static_weather_icon_label = ctk.CTkLabel(button_frame, text='') # Create icon label
static_weather_icon_label.pack(side=ctk.BOTTOM)
addns.weather(addns.load_settings()['city'], static_weather_icon_label)
###################################################################################################
# Запускаем распознавание речи в отдельном потоке
recognition_thread = threading.Thread(target=r.recognize_speech, args=(label, cmnds, outlabel, app, cmnds.slowly_output, weather_icon_label), daemon=True)
recognition_thread.start() # Start recognition

app.mainloop()