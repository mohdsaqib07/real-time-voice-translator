import os
import threading
import tkinter as tk
from gtts import gTTS
from tkinter import ttk
import speech_recognition as sr
from playsound import playsound
from deep_translator import GoogleTranslator
from google.transliteration import transliterate_text
import ttkbootstrap as tb
import sys
# from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.toast import ToastNotification
keep_running = False
# Create an instance of Tkinter frame or window
win= tb.Window(themename='pulse')

# Set the geometry of tkinter frame
win.geometry("1080x950")
win.title("Real-Time Voice🎙️ Translator🔊")
base_path = getattr(sys,'_MEIPATH','.') + '/'

# icon = tb.PhotoImage(file=f"{base_path}icon.png")
# win.iconphoto(True,icon)

# Create labels and text boxes for the recognized and translated text
input_label = tb.Label(win, text="Recognized Text ⮯",font=('Helvetica',18,'bold'))
input_label.pack()
input_text = tb.Text(win, height=10, width=50)
input_text.pack(pady=20)
def update_translation_on_click():
    global keep_running

    if keep_running:
        user_input_text = input_text.get("1.0", "end-1c")
        print(user_input_text)
        input_text_transliteration = transliterate_text(user_input_text, lang_code=input_lang.get()) if input_lang.get() not in ('auto', 'en') else user_input_text
        translated_text = GoogleTranslator(source=input_lang.get(), target=output_lang.get()).translate(text=input_text_transliteration)
        print(translated_text)
        if output_text.get('1.0','end-1c'):
            output_text.delete('1.0','end')
        output_text.insert(tb.END, translated_text + "\n")
        keep_running = False
def run_translator_on_click():
    global keep_running
    if not keep_running:
        keep_running = True
        update_translation_thread = threading.Thread(target=update_translation_on_click)        # using multi threading for efficient cpu usage
        update_translation_thread.start()
convert_button = tb.Button(master=win,text='Translate',command=run_translator_on_click,cursor='hand2',bootstyle='success') #type:ignore
convert_button.pack(pady=(0,10))

output_label = tb.Label(win, text="Translated Text ⮯",font=('Helvetica',18,'bold'))
output_label.pack()
output_text = tb.Text(win, height=10, width=50)
output_text.pack(pady=20)

blank_space = tb.Label(win, text="")
blank_space.pack()

# Create a dictionary of language names and codes
language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Spanish": "es",
    "Chinese (Simplified)": "zh-CN",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "German": "de",
    "French": "fr",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Punjabi": "pa"
}

language_names = list(language_codes.keys())

# Create dropdown menus for the input and output languages

input_lang_label = tb.Label(win, text="Select Input Language:",font=('Helvetica',18,'bold'))
input_lang_label.pack()

input_lang = tb.Combobox(win, values=language_names)
def update_input_lang_code(event):
    selected_language_name = event.widget.get()
    selected_language_code = language_codes[selected_language_name]
	# Update the selected language code
    input_lang.set(selected_language_code)
input_lang.bind("<<ComboboxSelected>>", lambda e: update_input_lang_code(e))
if input_lang.get() == "": input_lang.set("auto")
input_lang.pack()

down_arrow = tb.Label(win, text="▼")
down_arrow.pack()

output_lang_label = tb.Label(win, text="Select Output Language:",font=('Helvetical',18,'bold'))
output_lang_label.pack(pady=(10,0))

output_lang = tb.Combobox(win, values=language_names)
def update_output_lang_code(event):
    selected_language_name = event.widget.get()
    selected_language_code = language_codes[selected_language_name]
    # Update the selected language code
    output_lang.set(selected_language_code)
output_lang.bind("<<ComboboxSelected>>", lambda e: update_output_lang_code(e))
if output_lang.get() == "": output_lang.set("en")
output_lang.pack()

blank_space = tb.Label(win, text="")
blank_space.pack(pady=20)


def update_translation():
    global keep_running

    if keep_running:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Speak Now!\n")
            audio = r.listen(source)
            
            try: 
                speech_text = r.recognize_google(audio) #type:ignore
                print(speech_text) 
                # print(speech_text)
                speech_text_transliteration = transliterate_text(speech_text, lang_code=input_lang.get()) if input_lang.get() not in ('auto', 'en') else speech_text
                input_text.insert(tb.END,'')
                input_text.insert(tb.END, f"{speech_text_transliteration}\n")
                if 'exit' in speech_text.lower():
                    print('translation stops now')
                    #keep_running = False
                    kill_execution()
                    return
                elif 'stop' in speech_text.lower():
                    print('translation stops now')
                    kill_execution()
                    # keep_running = False
                    return
             

                
                translated_text = GoogleTranslator(source=input_lang.get(), target=output_lang.get()).translate(text=speech_text_transliteration)
                # print(translated_text)

                voice = gTTS(translated_text, lang=output_lang.get())
                if not os.path.exists('voice.mp3'):
                    voice.save('voice.mp3')
                    playsound('voice.mp3')
                    # os.remove('voice.mp3')
                else:
                    files = [ f for f in os.listdir() if f.endswith('.mp3')]
                    length = len(files)
                    voice.save(f'voice{length}.mp3')
                    playsound(f'voice{length}.mp3')
                    # os.remove(f'voice{length}.mp3')

                output_text.insert(tb.END,'')
                output_text.insert(tb.END, translated_text + "\n")
                
            except sr.UnknownValueError:
                output_text.insert(tb.END, "Could not understand!\n")
            except sr.RequestError:
                output_text.insert(tb.END, "Could not request from Google!\n")

    win.after(100, update_translation)


def run_translator():
    global keep_running
    
    if not keep_running:
        keep_running = True
        update_translation_thread = threading.Thread(target=update_translation)        # using multi threading for efficient cpu usage
        update_translation_thread.start()




def kill_execution():
    global keep_running
    keep_running = False
    toast = ToastNotification(title='The Interpreter',message='Tranlation Stops Now!',duration=3000,alert=True)
    toast.show_toast()
    # mb = Messagebox.ok(message='Tranlation Stops',title='Stop',alert=True)

def open_about_page():      # about page
    about_window = tb.Toplevel()
    about_window.title("About")
    # about_window.iconphoto(False, icon)

    # Create a link to the GitHub repository
    github_link = tb.Label(about_window, text="https://github.com/mohdsaqib07/real-time-voice-translator", underline=True, foreground="blue", cursor="hand2")
    github_link.bind("<Button-1>", lambda e: open_webpage("https://github.com/mohdsaqib07/real-time-voice-translator"))
    github_link.pack()

    # Create a text widget to display the about text
    about_text = tb.Text(about_window, height=10, width=50)
    about_text.insert("1.0", """
    A machine learning project that translates voice from one language to another in real time while preserving the tone and emotion of the speaker, and outputs the result in MP3 format. Choose input and output languages from the dropdown menu and start the translation!
    """)
    about_text.pack()

    # Create a "Close" button
    close_button = tb.Button(bootstyle='success',master=about_window,cursor='hand2', text="Close", command=about_window.destroy) #type:ignore
    close_button.pack()

def open_webpage(url):      # Opens a web page in the user's default web browser.
    import webbrowser
    webbrowser.open(url)



# Create the "Run" button
run_button = tb.Button(bootstyle='success',master=win,cursor='hand2', text="Start Translation", command=run_translator) #type:ignore
run_button.place(relx=0.25, rely=0.95, anchor=tk.CENTER) #type:ignore

# Create the "Kill" button
kill_button = tb.Button(bootstyle='success',master=win,cursor='hand2', text="Stop Translation", command=kill_execution) #type:ignore
kill_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER) #type:ignore

# Open about page button
about_button = tb.Button(bootstyle='success',master=win, text="About this project", command=open_about_page) #type:ignore
about_button.place(relx=0.75, rely=0.95, anchor=tk.CENTER) #type:ignore

# Run the Tkinter event loop
win.resizable(False,False)
win.mainloop()
