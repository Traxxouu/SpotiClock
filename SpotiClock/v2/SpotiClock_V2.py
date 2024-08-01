import time
import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import webbrowser
import pytz
import json
import os

# Fichier de configuration
CONFIG_FILE = "alarm_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            hour.set(config.get("hour", "00"))
            minute.set(config.get("minute", "00"))
            second.set(config.get("second", "00"))
            spotify_url.set(config.get("spotify_url", ""))
            mouse_x.set(config.get("mouse_x", "0"))
            mouse_y.set(config.get("mouse_y", "0"))

def save_config():
    config = {
        "hour": hour.get(),
        "minute": minute.get(),
        "second": second.get(),
        "spotify_url": spotify_url.get(),
        "mouse_x": mouse_x.get(),
        "mouse_y": mouse_y.get()
    }
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)

# position de la souris
def seconde_fenetre():
    messagebox.showinfo("Information", "Vous avez 6 secondes pour placer votre souris après avoir fermé la fenêtre. \n🛡️ Ne bougez plus votre souris après l'avoir placée.")
    root.after(6000, position_souris)

def position_souris():
    current_mouse_position = pyautogui.position()
    mouse_x.set(current_mouse_position[0])
    mouse_y.set(current_mouse_position[1])
    messagebox.showinfo("Position actuelle", f"La position de votre souris est : {current_mouse_position}")
    print(f"Position actuelle de la souris : {current_mouse_position}")

# alarme
def set_alarm():
    alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"
    messagebox.showinfo("Alarme réglée", f"Alarme réglée à {alarm_time}")
    alarm_thread = threading.Thread(target=check_alarm, args=(alarm_time,))
    alarm_thread.start()
    save_config()

def check_alarm(alarm_time):
    while True:
        now = datetime.now(pytz.timezone('Europe/Paris')).strftime("%H:%M:%S")
        if now == alarm_time:
            launch_spotify()
            break
        time.sleep(1)

def launch_spotify():
    url = spotify_url.get()
    if not url:
        messagebox.showerror("Erreur", "Veuillez entrer une URL de playlist Spotify.")
        return
    webbrowser.open(url)
    time.sleep(10)  # Attendre que la page Spotify se charge
    move_mouse_and_click(int(mouse_x.get()), int(mouse_y.get()))
    messagebox.showinfo("Alarme", "Il est temps de se réveiller!")

def move_mouse_and_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()

# Interface UI
root = tk.Tk()
root.title("⏰ Spotify Réveille ⏰")
root.geometry("600x460")
root.resizable(False, False)

style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))
style.configure("TCombobox", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))

# Contenu fenêtre - position de la souris
ttk.Label(root, text="Trouver la position de sa souris", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(20, 10))
ttk.Button(root, text="Commencer", command=seconde_fenetre).grid(row=1, column=0, columnspan=2, pady=(0, 20))

# TITRE
ttk.Label(root, text="Réglage de l'alarme", font=("Helvetica", 14, "bold")).grid(row=2, column=0, columnspan=2, pady=(10, 10))

# Contenu fenêtre pour l'alarme
ttk.Label(root, text="Heure (HH)").grid(row=3, column=0, padx=10, pady=5)
ttk.Label(root, text="Minute (MM)").grid(row=4, column=0, padx=10, pady=5)
ttk.Label(root, text="Seconde (SS)").grid(row=5, column=0, padx=10, pady=5)
ttk.Label(root, text="URL de la playlist Spotify").grid(row=6, column=0, padx=10, pady=5)
ttk.Label(root, text="Position X de la souris").grid(row=7, column=0, padx=10, pady=5)
ttk.Label(root, text="Position Y de la souris").grid(row=8, column=0, padx=10, pady=5)

hour = tk.StringVar()
minute = tk.StringVar()
second = tk.StringVar()
spotify_url = tk.StringVar()
mouse_x = tk.StringVar()
mouse_y = tk.StringVar()

hours = [f"{i:02}" for i in range(24)]
minutes_seconds = [f"{i:02}" for i in range(60)]

hour_combobox = ttk.Combobox(root, textvariable=hour, values=hours, state="readonly", width=5)
minute_combobox = ttk.Combobox(root, textvariable=minute, values=minutes_seconds, state="readonly", width=5)
second_combobox = ttk.Combobox(root, textvariable=second, values=minutes_seconds, state="readonly", width=5)

hour_combobox.grid(row=3, column=1, padx=10, pady=5)
minute_combobox.grid(row=4, column=1, padx=10, pady=5)
second_combobox.grid(row=5, column=1, padx=10, pady=5)

url_entry = ttk.Entry(root, textvariable=spotify_url, width=40)
url_entry.grid(row=6, column=1, padx=10, pady=5)

x_entry = ttk.Entry(root, textvariable=mouse_x, width=10)
x_entry.grid(row=7, column=1, padx=10, pady=5)

y_entry = ttk.Entry(root, textvariable=mouse_y, width=10)
y_entry.grid(row=8, column=1, padx=10, pady=5)

ttk.Button(root, text="Régler l'alarme", command=set_alarm).grid(row=9, columnspan=2, pady=20)

# Charger les paramètres sauvegardés au démarrage
load_config()

# Sauvegarder les paramètres à la fermeture
root.protocol("WM_DELETE_WINDOW", lambda: (save_config(), root.destroy()))

root.mainloop()
