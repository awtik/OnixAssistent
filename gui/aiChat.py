import customtkinter as ctk
import asyncio
from modules.gptResponse import get_answer
from modules.addons import Addons
addns = Addons()
# AI chat window
def show_ai_chat(app):
    "Open AI chat window"
    # Window Settings
    ai_window = ctk.CTkToplevel(app) # Create Toplevel window for AI chat
    ai_window.geometry("450x350") # Set size for AI chat
    ai_window.title("AI Chat") # Set title
    ai_window.resizable(False, False) # Disable resize function
    ai_window.grab_set() # Disable interaction with other windows
    # Textbox for chat
    response_textbox = ctk.CTkTextbox(ai_window, wrap='word', width=400, height=250) # Create a textbox and set size
    response_textbox.pack(padx=10, pady=10)
    response_textbox.configure(state="disabled") # Disable interacting with textbox
    # Prompt Entrybox
    entry = ctk.CTkEntry(ai_window, width=400) # Create entry
    entry.pack(padx=10, pady=(0, 10))
    entry.bind('<Return>', lambda event: asyncio.run(send_message(entry, response_textbox, ai_window))) # IF keydown Enter - start send_message
    # Clear Chat button
    clear_button = ctk.CTkButton(ai_window, text="Clear chat", command=lambda: clear_chat(response_textbox)) # Create button for clear chat
    clear_button.pack(pady=5, anchor='w', padx=25)
    addns.check_transparency_enable(ai_window) # Adding style for app

async def type_text(widget, text, delay=0.001):
    "Function for slowing print the text in AI Chat"
    for char in text:
        widget.insert('end', char) # Insert char into textbox
        widget.update() # Update textbox
        widget.see('end') # automatic scrolling to the end
        await asyncio.sleep(delay) # Delay

async def send_message(entry, textbox, app):
    "function for send_message in AI chat"
    prompt = entry.get() # Get prompt from entry
    if prompt.lower() == 'stop chat': # Stop chatting
        app.destroy() # Quit from AI chat
        return

    entry.delete(0, 'end') # Clear entry box
    textbox.configure(state="normal") # Set normal state for textbox
    textbox.insert('end', f"Вы: {prompt}\n\n") # Insert user msg into textbox
    textbox.see('end') # automatic scrolling to the end

    response = 'AI: '+ await get_answer(prompt) # Get answer from AI
    await type_text(textbox, response, delay=0.02) # Slowing print AI's answer
    print('')
    textbox.configure(state="disabled") # Disable interacting with textbox again
    
def clear_chat(textbox):
    "Function for clear AI chat"
    textbox.configure(state='normal')
    textbox.delete("1.0", 'end')
    textbox.configure(state="disabled") # Disable interacting with textbox again
