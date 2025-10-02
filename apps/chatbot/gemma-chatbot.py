import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

# === Jalankan model Ollama "gemma:2b" secara otomatis ===
def ensure_ollama_gemma():
    try:
        subprocess.Popen(["ollama", "run", "gemma:2b"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print("❌ Gagal menjalankan Ollama Gemma:", e)

# === Kirim prompt ke Gemma tanpa timeout ===
def ask_ollama_gemma(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma:2b"],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = result.stdout.decode().strip()
        return output
    except Exception as e:
        return f"⚠️ Error: {e}"

# === Fungsi kirim pesan (multithread agar tidak freeze UI) ===
def send_message(event=None):
    user_input = entry.get()
    if not user_input.strip():
        return

    chat_box.insert(tk.END, "You:\n", "user_label")
    chat_box.insert(tk.END, f"{user_input}\n\n", "user_msg")
    entry.delete(0, tk.END)
    chat_box.yview(tk.END)

    # Placeholder "Gemma is thinking..."
    thinking_index = chat_box.index(tk.END)
    chat_box.insert(tk.END, "Gemma:\n", "bot_label")
    chat_box.insert(tk.END, "... is thinking\n\n", "bot_msg")
    chat_box.yview(tk.END)

    def process():
        bot_reply = ask_ollama_gemma(user_input)

        # Hapus placeholder dan masukkan jawaban asli
        chat_box.delete(thinking_index, tk.END)
        chat_box.insert(tk.END, "Gemma:\n", "bot_label")
        chat_box.insert(tk.END, f"{bot_reply}\n\n", "bot_msg")
        chat_box.yview(tk.END)

    threading.Thread(target=process).start()

# === Setup UI ===
window = tk.Tk()
window.title("🤖 Gemma 2B Chat (Ollama)")
window.geometry("700x600")
window.configure(bg="#121212")

# Chat Box
chat_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, bg="#1e1e1e", fg="#f5f5f5",
                                     font=("Segoe UI", 11), padx=15, pady=10)
chat_box.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Style tags
chat_box.tag_config("user_label", foreground="#60a5fa", font=("Segoe UI", 10, "bold"))
chat_box.tag_config("user_msg", foreground="#ffffff", font=("Segoe UI", 11))
chat_box.tag_config("bot_label", foreground="#facc15", font=("Segoe UI", 10, "bold"))
chat_box.tag_config("bot_msg", foreground="#e2e8f0", font=("Segoe UI", 11))

chat_box.insert(tk.END, "✨ Gemma 2B Local Chat is ready!\n", "bot_msg")
chat_box.insert(tk.END, "Tanyakan sesuatu di bawah ini...\n\n", "bot_msg")

# Input field
entry_frame = tk.Frame(window, bg="#121212")
entry_frame.pack(padx=20, pady=10, fill=tk.X)

entry = tk.Entry(entry_frame, font=("Segoe UI", 12), bg="#1e1e1e", fg="#f5f5f5", insertbackground="white")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry.bind("<Return>", send_message)

send_btn = tk.Button(entry_frame, text="Send", command=send_message,
                     bg="#facc15", fg="#0f172a", font=("Segoe UI", 10, "bold"), padx=14, pady=6)
send_btn.pack(side=tk.RIGHT)

# Jalankan model saat aplikasi dibuka
ensure_ollama_gemma()

# Start app
window.mainloop()
