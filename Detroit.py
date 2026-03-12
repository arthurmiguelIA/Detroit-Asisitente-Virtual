import os
import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import datetime
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
from queue import Queue
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

wikipedia.set_lang("pt")

voice_queue = Queue()

def speak_worker():
    while True:
        text = voice_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        voice_queue.task_done()

Thread(target=speak_worker, daemon=True).start()

def speak(text):
    chat_area.configure(state='normal')
    chat_area.insert(tk.END, "Detroit: " + text + "\n")
    chat_area.see(tk.END)
    chat_area.configure(state='disabled')
    voice_queue.put(text)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5)
            return r.recognize_google(audio, language="pt-BR").lower()
        except:
            return ""

def handle_command(command):

    if "google" in command:
        speak("Abrindo Google")
        webbrowser.open("https://google.com")

    elif "youtube" in command:
        speak("Abrindo YouTube")
        webbrowser.open("https://youtube.com")

    elif "instagram" in command:
        speak("Abrindo Instagram")
        webbrowser.open("https://instagram.com")

    elif "whatsapp" in command:
        speak("Abrindo WhatsApp")
        webbrowser.open("https://web.whatsapp.com")

    elif "chat gpt" in command:
        speak("Abrindo chat gpt")
        webbrowser.open("https://chat.openai.com")

    elif "github" in command:
        speak("Abrindo GitHub")
        webbrowser.open("https://github.com")

    elif "linkedin" in command:
        speak("Abrindo LinkedIn")
        webbrowser.open("https://linkedin.com")

    elif "gmail" in command:
        speak("Abrindo Gmail")
        webbrowser.open("https://mail.google.com")

    elif "netflix" in command:
        speak("Abrindo Netflix")
        webbrowser.open("https://netflix.com")

    elif "spotify" in command:
        speak("Abrindo Spotify")
        os.system("start spotify")

    elif "vscode" in command or "visual studio code" in command:
        speak("Abrindo Visual Studio Code")
        os.system("code")

    elif "calculadora" in command:
        speak("Abrindo calculadora")
        os.system("calc")

    elif "bloco de notas" in command:
        speak("Abrindo bloco de notas")
        os.system("notepad")

    elif "explorador" in command or "arquivos" in command:
        speak("Abrindo explorador de arquivos")
        os.system("explorer")

    elif "wikipedia" in command or "wikipédia" in command:
        speak("O que você quer pesquisar?")
        query = listen()
        if query:
            try:
                result = wikipedia.summary(query, sentences=2)
                speak(result)
            except:
                speak("Não encontrei resultados")

    elif "horas" in command or "que horas são" in command:
        hora = datetime.datetime.now().strftime("%H:%M")
        speak(f"Agora são {hora}")

    elif "tchau" in command or "encerrar" in command:
        speak("Até logo")
        return False

    else:
        speak("Não entendi, tente novamente")

    return True

def start_voice_assistant():
    speak("Detroit ativada")
    running = True
    while running:
        command = listen()
        if command:
            chat_area.configure(state='normal')
            chat_area.insert(tk.END, "Você: " + command + "\n")
            chat_area.see(tk.END)
            chat_area.configure(state='disabled')
            running = handle_command(command)
        else:
            time.sleep(0.2)

def send_text_command():
    command = entry.get().strip().lower()
    if command:
        chat_area.configure(state='normal')
        chat_area.insert(tk.END, "Você: " + command + "\n")
        chat_area.see(tk.END)
        chat_area.configure(state='disabled')
        entry.delete(0, tk.END)
        handle_command(command)

window = tk.Tk()
window.title("Detroit Assistente")
window.geometry("500x400")

chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='disabled')
chat_area.pack(expand=True, fill='both')

entry_frame = tk.Frame(window)
entry_frame.pack(fill='x', padx=5, pady=5)

entry = tk.Entry(entry_frame)
entry.pack(side='left', expand=True, fill='x', padx=(0,5))

send_button = tk.Button(entry_frame, text="Enviar", command=send_text_command)
send_button.pack(side='right')

Thread(target=start_voice_assistant, daemon=True).start()

window.mainloop()