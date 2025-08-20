import speech_recognition as sr
import tkinter as tk
from deep_translator import GoogleTranslator
import datetime

# 🎙️ Speech recognizer setup
recognizer = sr.Recognizer()
mic = sr.Microphone()

# 🌐 Translator setup (English → Hindi)
translator = GoogleTranslator(source="en", target="hi")

# 🖼️ GUI Setup
root = tk.Tk()
root.title("Smart Edu-Glasses Subtitle Simulator")
root.geometry("700x400")
root.config(bg="black")

title = tk.Label(root, text="Smart Edu-Glasses", font=("Arial", 22, "bold"), fg="cyan", bg="black")
title.pack(pady=5)

subtitle_label = tk.Label(root, text="🎤 Speak something...", font=("Arial", 18), fg="lime", bg="black", wraplength=650, justify="center")
subtitle_label.pack(pady=10)

history_box = tk.Text(root, height=10, width=70, font=("Arial", 12), fg="white", bg="black")
history_box.pack(pady=10)

def clear_history():
    history_box.delete("1.0", tk.END)

clear_btn = tk.Button(root, text="Clear Subtitles", command=clear_history, bg="red", fg="white", font=("Arial", 12))
clear_btn.pack(pady=5)

# 📁 Save transcript
transcript_file = open("transcript.txt", "a", encoding="utf-8")
transcript_file.write("\n\n=== New Session Started: " + str(datetime.datetime.now()) + " ===\n")

def listen_and_update():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)  
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)  # Speech → Text

            # Translate to Hindi
            translated = translator.translate(text)

            # Update GUI
            subtitle_label.config(text=text)
            history_box.insert(tk.END, "EN: " + text + "\nHI: " + translated + "\n\n")
            history_box.see(tk.END)  # auto-scroll

            # Save to file
            transcript_file.write("EN: " + text + " | HI: " + translated + "\n")
            transcript_file.flush()

            print("✅ You said:", text)

        except sr.UnknownValueError:
            subtitle_label.config(text="⚠️ Could not understand...")
        except sr.RequestError:
            subtitle_label.config(text="⚠️ Speech Recognition API error!")

    root.after(200, listen_and_update)

# Start speech recognition loop
root.after(1000, listen_and_update)
root.mainloop()

transcript_file.close()
