import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

# === Fungsi untuk jalankan ollama run mistral secara otomatis ===
def ensure_ollama_model():
    try:
        subprocess.Popen(["ollama", "run", "mistral"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print("❌ Gagal menjalankan Ollama Mistral:", e)

# === Fungsi untuk kirim pesan ke Mistral tanpa timeout ===
def ask_ollama(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # ❌ HAPUS timeout
        )
        output = result.stdout.decode().strip()
        return output
    except Exception as e:
        return f"⚠️ Error: {e}"

# === Fungsi event kirim (threaded untuk hindari freeze UI) ===
def send_message(event=None):
    user_input = entry.get()
    if not user_input.strip():
        return

    chat_box.insert(tk.END, f"You:\n", "user_label")
    chat_box.insert(tk.END, f"{user_input}\n\n", "user_msg")
    entry.delete(0, tk.END)
    chat_box.yview(tk.END)

    thinking_index = chat_box.index(tk.END)
    chat_box.insert(tk.END, "Mistral:\n", "bot_label")
    chat_box.insert(tk.END, "... is thinking\n\n", "bot_msg")
    chat_box.yview(tk.END)

    def process():
        bot_reply = ask_ollama(user_input)

        # Hapus teks thinking
        chat_box.delete(thinking_index, tk.END)

        # Masukkan jawaban
        chat_box.insert(tk.END, f"Mistral:\n", "bot_label")
        chat_box.insert(tk.END, f"{bot_reply}\n\n", "bot_msg")
        chat_box.yview(tk.END)

    threading.Thread(target=process).start()

# === Setup UI ===
window = tk.Tk()
window.title("🧠 Mistral Local Chat")
window.geometry("700x600")
window.configure(bg="#121212")

chat_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, bg="#1e1e1e", fg="#f5f5f5",
                                     font=("Segoe UI", 11), padx=15, pady=10, state=tk.NORMAL)
chat_box.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Style
chat_box.tag_config("user_label", foreground="#60a5fa", font=("Segoe UI", 10, "bold"))
chat_box.tag_config("user_msg", foreground="#ffffff", font=("Segoe UI", 11))
chat_box.tag_config("bot_label", foreground="#22c55e", font=("Segoe UI", 10, "bold"))
chat_box.tag_config("bot_msg", foreground="#d4d4d4", font=("Segoe UI", 11))

chat_box.insert(tk.END, "✨ Mistral Chat (Ollama) Ready\n", "bot_msg")
chat_box.insert(tk.END, "Tanyakan sesuatu di bawah ini...\n\n", "bot_msg")

# Input
entry_frame = tk.Frame(window, bg="#121212")
entry_frame.pack(padx=20, pady=10, fill=tk.X)

entry = tk.Entry(entry_frame, font=("Segoe UI", 12), bg="#1e1e1e", fg="#f5f5f5", insertbackground="white")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry.bind("<Return>", send_message)  # Tombol Enter ↵

send_btn = tk.Button(entry_frame, text="Send", command=send_message, bg="#22c55e",
                     fg="#121212", font=("Segoe UI", 10, "bold"), padx=14, pady=6)
send_btn.pack(side=tk.RIGHT)

# Jalankan model lokal saat aplikasi dimulai
ensure_ollama_model()

window.mainloop()
