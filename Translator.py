# Imports
import json
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import code_engine
import sys
from PIL import Image
# from tkfontawesome import icon_to_image
import os
import customtkinter as ctk
# Constants
FileURL = ""
if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.abspath(__file__))
languages = []
for i in os.listdir(f"{app_path}/data"):
    if not ".png" in i and not ".ico" in i:
        languages.append(i.replace("_KW.json", ""))
        #print(i.replace("_KW.json", ""))
        #print(languages)

# GUI
root = ctk.CTk()
root.title("World Translator")
root.update()
root.iconbitmap(f"{app_path}/data/world.ico")
#root.attributes('-alpha', 0.95)
width = root.winfo_width()
ctk.set_appearance_mode("Dark")
open_button = ctk.CTkButton(root, text="OpenFile", width=300, height=30, cursor="hand2")
open_button.grid(row=0, column=0)
modeimg = ctk.CTkImage(Image.open(f"{app_path}/data/mode.png"), size=(80, 30))
mode_button = ctk.CTkButton(root, text="", image=modeimg, width=100, height=30, fg_color="transparent", cursor="hand2",
                            hover_color="white")
mode_button.grid(row=0, column=1)
logo = ctk.CTkImage(Image.open(f"{app_path}/data/world.png"), size=(300, 300))
ctk.CTkLabel(root, image=logo, text="").grid(row=1, column=0, columnspan=2)

lang = StringVar()
myframe = ctk.CTkFrame(root, width=width-100, corner_radius=10)
myframe.grid(row=2, column=0, columnspan=3, pady=5)
ctk.CTkLabel(myframe, text="Select Language", justify="center").grid(row=2, column=0, columnspan=2)
language = ttk.Combobox(myframe, values=languages, width=52, state="readonly", textvariable=lang)
language.grid(row=3, column=0, columnspan=2, padx=20, pady=5)
language.current(0)
translate_button = ctk.CTkButton(myframe, text="Translate", width=370)
translate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

#root.attributes("-cornerradius", 10)


def switch_mode():
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        mode_button.configure(hover_color="black")
    else:
        mode_button.configure(hover_color="white")
        ctk.set_appearance_mode("Dark")


def openfile():
    global FileURL
    file = filedialog.askopenfilename(filetypes=[("World Files", "*.world"), ("All Files", "*.*")])
    FileURL = file
    print(FileURL)


def Offline_translate():
    # getting current language trans and putting it in a dict
    if lang.get() == "":
        messagebox.showerror(title="Error", message="Please select a langauge first")
    if FileURL == "":
        messagebox.showerror(title="Error", message="Please chose a file")
    else:
        with open(FileURL, "r", encoding="utf-8") as f:
            code = f.read()
            # print(code)
        with open("translated_code.world", "w", encoding="utf-8") as file:
            translated_code = code_engine.Translate(code)
            print(lang.get())
            file.truncate()
            file.write(translated_code.read(lang.get()))
        with open(f"{app_path}/data/{lang.get()}_KW.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            with open(f"{app_path}/keywords.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
                messagebox.showinfo(title="success", message="Successfully translated keywords")


translate_button.configure(command=Offline_translate)
open_button.configure(command=openfile)
mode_button.configure(command=switch_mode)
root.mainloop()
