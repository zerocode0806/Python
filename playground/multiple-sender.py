import pyautogui
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import os

# --- Send Function ---
def send_messages():
    contacts = contact_input.get("1.0", tk.END).strip().splitlines()
    message = message_input.get("1.0", tk.END).strip()

    if not contacts or not message:
        messagebox.showwarning("Perhatian", "Kontak dan pesan tidak boleh kosong.")
        return

    # --- Open WhatsApp Desktop (Microsoft Store version) ---
    try:
        subprocess.Popen("explorer shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App", shell=True)
        # messagebox.showinfo("Membuka WhatsApp", "WhatsApp Desktop dibuka. Tunggu 3 detik...")
        time.sleep(3)
    except Exception as e:
        messagebox.showerror("Gagal Membuka WhatsApp", f"Pastikan WhatsApp terinstall.\n\n{e}")
        return

    # --- Mulai Kirim Pesan ---
    for contact in contacts:
        pyautogui.click(x=219, y=182)  # ← Ubah jika posisi search bar beda
        time.sleep(0.5)
        pyautogui.write(contact, interval=0.03)
        time.sleep(1)
        pyautogui.press("down")
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.write(message, interval=0.02)
        pyautogui.press("enter")
        time.sleep(1.5)

    messagebox.showinfo("Done", "✅ All message sent.")

# --- UI Setup ---
app = tk.Tk()
app.title("💬 WA Auto-Sender Bot")
app.geometry("500x550")
app.configure(bg="#1e1e1e")

title = tk.Label(app, text="💬 WhatsApp Message Bot", font=("Segoe UI", 16, "bold"), fg="#00ffaa", bg="#1e1e1e")
title.pack(pady=10)

# Kontak input
tk.Label(app, text="🧑 Contact List (per one line):", fg="#ffffff", bg="#1e1e1e", anchor="w").pack(fill="x", padx=20)
contact_input = scrolledtext.ScrolledText(app, height=8, font=("Consolas", 11), bg="#2e2e2e", fg="#ffffff", insertbackground="white")
contact_input.pack(fill="both", padx=20, pady=(0,10))

# Pesan input
tk.Label(app, text="✉️ Message that you want to send:", fg="#ffffff", bg="#1e1e1e", anchor="w").pack(fill="x", padx=20)
message_input = scrolledtext.ScrolledText(app, height=6, font=("Consolas", 11), bg="#2e2e2e", fg="#ffffff", insertbackground="white")
message_input.pack(fill="both", padx=20, pady=(0,10))

# Tombol kirim
send_button = tk.Button(app, text="🚀 Send Message", font=("Segoe UI", 12, "bold"),
                        command=send_messages, bg="#00ffaa", fg="#000000", activebackground="#00ddaa")
send_button.pack(pady=20)

# Footer
footer = tk.Label(app, text="Created by You with 💻 Python & PyAutoGUI", fg="#888888", bg="#1e1e1e", font=("Segoe UI", 8))
footer.pack(side="bottom", pady=5)

app.mainloop()