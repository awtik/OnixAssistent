import customtkinter as ctk
import asyncio
from modules.gpt_response import get_answer
from modules.addons import Addons

addons = Addons()

def show_ai_chat(main_app):
    ai_window = ctk.CTkToplevel(main_app)
    ai_window.geometry("450x350")
    ai_window.title("AI Chat")
    ai_window.resizable(False, False)
    ai_window.grab_set()

    chat_textbox = ctk.CTkTextbox(
        ai_window, wrap="word", width=400, height=250
    )
    chat_textbox.pack(padx=10, pady=10)
    chat_textbox.configure(state='disabled')
    
    prompt_entry = ctk.CTkEntry(ai_window, width=400)
    prompt_entry.pack(padx=10, pady=(0, 10))
    prompt_entry.bind(
        "<Return>", 
        lambda event: asyncio.run(send_message(prompt_entry, chat_textbox, ai_window))
    )

    clear_button = ctk.CTkButton(
        ai_window, text="Clear chat", command=lambda: clear_chat(chat_textbox)
    )
    clear_button.pack(pady=5, anchor="w", padx=25)

    addons.check_transparency_enable(ai_window)

async def type_text(widget, response_text, delay=0.001):
    """Print text in AI chat with a delay between each character."""
    
    for char in response_text:
        widget.insert("end", char)
        widget.update()
        widget.see("end")
        await asyncio.sleep(delay)

async def send_message(prompt_entry, chat_textbox, ai_window):
    """Send message in AI chat and display the AI's response."""
    
    prompt = prompt_entry.get()
    if prompt.lower() == "stop chat":
        ai_window.destroy()
        return

    prompt_entry.delete(0, "end")
    chat_textbox.configure(state='normal')
    chat_textbox.insert("end", f"Вы: {prompt}\n\n")
    chat_textbox.see("end")

    response_text = "AI: " + get_answer(prompt) + "\n"
    await type_text(chat_textbox, response_text, delay=0.02)
    chat_textbox.configure(state='disabled')

def clear_chat(chat_textbox):
    chat_textbox.configure(state='normal')
    chat_textbox.delete("1.0", "end")
    chat_textbox.configure(state='disabled')