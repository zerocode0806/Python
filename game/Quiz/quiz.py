import tkinter as tk
from tkinter import messagebox
import random
import time

# Daftar pertanyaan (kategori: pertanyaan, jawaban)
questions = {
    "Sains": [
        {"pertanyaan": "Apa unsur kimia dengan simbol H?", "jawaban": "hidrogen"},
        {"pertanyaan": "Berapa planet di tata surya kita?", "jawaban": "8"},
        {"pertanyaan": "Siapa penemu teori relativitas?", "jawaban": "einstein"},
        {"pertanyaan": "Apa nama planet terdekat dengan matahari?", "jawaban": "merkurius"},
        {"pertanyaan": "Berapa lama satu hari di bumi?", "jawaban": "24 jam"},
        {"pertanyaan": "Apa nama gas yang kita hirup untuk bernapas?", "jawaban": "oksigen"},
        {"pertanyaan": "Berapakah jarak rata-rata antara bumi dan matahari?", "jawaban": "149,6 juta km"},
        {"pertanyaan": "Apa unsur kimia dengan simbol O?", "jawaban": "oksigen"},
        {"pertanyaan": "Apa nama sel darah yang membawa oksigen?", "jawaban": "sel darah merah"},
        {"pertanyaan": "Siapa penemu lampu pijar?", "jawaban": "thomas edison"},
        {"pertanyaan": "Apa nama planet terbesar di tata surya?", "jawaban": "jupiter"},
        {"pertanyaan": "Apa nama fenomena alam saat bulan menutupi matahari?", "jawaban": "gerhana matahari"},
        {"pertanyaan": "Berapa kecepatan cahaya dalam km per detik?", "jawaban": "300000 km/s"},
        {"pertanyaan": "Apa nama molekul yang membawa informasi genetik?", "jawaban": "dna"},
        {"pertanyaan": "Berapakah pH air murni?", "jawaban": "7"},
        {"pertanyaan": "Apa nama alat yang digunakan untuk mengukur gempa bumi?", "jawaban": "seismograf"},
        {"pertanyaan": "Apa planet ketiga dari matahari?", "jawaban": "bumi"},
        {"pertanyaan": "Apa nama partikel bermuatan negatif dalam atom?", "jawaban": "elektron"},
        {"pertanyaan": "Siapa penemu pesawat terbang?", "jawaban": "wright bersaudara"},
        {"pertanyaan": "Apa nama reaksi kimia yang menghasilkan panas?", "jawaban": "reaksi eksoterm"},
        {"pertanyaan": "Apa nama lapisan terluar bumi?", "jawaban": "kerak bumi"},
        {"pertanyaan": "Apa nama alat yang digunakan untuk mengukur suhu?", "jawaban": "termometer"},
        {"pertanyaan": "Apa unsur kimia dengan simbol Au?", "jawaban": "emas"},
        {"pertanyaan": "Apa nama teori yang menjelaskan asal usul alam semesta?", "jawaban": "big bang"},
        {"pertanyaan": "Apa nama proses perubahan dari cair menjadi gas?", "jawaban": "penguapan"},
        {"pertanyaan": "Siapa penemu hukum gravitasi?", "jawaban": "isaac newton"},
        {"pertanyaan": "Apa nama reaksi kimia yang terjadi saat besi berkarat?", "jawaban": "oksidasi"},
        {"pertanyaan": "Apa nama planet terdingin di tata surya?", "jawaban": "uranus"},
        {"pertanyaan": "Apa nama elemen paling ringan?", "jawaban": "hidrogen"},
        {"pertanyaan": "Apa nama hewan mamalia terbesar di dunia?", "jawaban": "paus biru"},
        {"pertanyaan": "Apa nama organ yang memompa darah ke seluruh tubuh?", "jawaban": "jantung"},
        {"pertanyaan": "Apa nama proses perubahan dari padat menjadi cair?", "jawaban": "mencair"},
        {"pertanyaan": "Siapa penemu telepon?", "jawaban": "alexander graham bell"},
        {"pertanyaan": "Apa nama planet keempat dari matahari?", "jawaban": "mars"}
    ],
    "Sejarah": [
        {"pertanyaan": "Siapa presiden pertama Indonesia?", "jawaban": "soekarno"},
        {"pertanyaan": "Tahun berapa Perang Dunia II berakhir?", "jawaban": "1945"},
        {"pertanyaan": "Apa nama kerajaan terbesar di Indonesia?", "jawaban": "majapahit"},
        {"pertanyaan": "Siapa penemu Amerika?", "jawaban": "kristoforus kolombus"},
        {"pertanyaan": "Tahun berapa Indonesia merdeka?", "jawaban": "1945"},
        {"pertanyaan": "Apa nama perang yang melibatkan Amerika Serikat dan Vietnam?", "jawaban": "perang vietnam"},
        {"pertanyaan": "Siapa penulis naskah proklamasi kemerdekaan Indonesia?", "jawaban": "soekarno-hatta"},
        {"pertanyaan": "Siapa presiden Amerika Serikat saat Perang Dunia II?", "jawaban": "franklin d. roosevelt"},
        {"pertanyaan": "Apa nama dinasti yang memerintah Tiongkok selama lebih dari 400 tahun?", "jawaban": "dinasti han"},
        {"pertanyaan": "Apa nama ibukota Kekaisaran Romawi Timur?", "jawaban": "konstantinopel"},
        {"pertanyaan": "Siapa yang memimpin Perang Kemerdekaan India melawan Inggris?", "jawaban": "mahatma gandhi"},
        {"pertanyaan": "Siapa raja terkenal dari kerajaan Mesir kuno?", "jawaban": "raja tutankhamun"},
        {"pertanyaan": "Kapan Revolusi Prancis terjadi?", "jawaban": "1789"},
        {"pertanyaan": "Siapa pahlawan wanita yang memimpin perang melawan Prancis di abad ke-15?", "jawaban": "joan of arc"},
        {"pertanyaan": "Apa nama penakluk terkenal dari Makedonia?", "jawaban": "alexander agung"},
        {"pertanyaan": "Siapa pemimpin Jerman selama Perang Dunia II?", "jawaban": "adolf hitler"},
        {"pertanyaan": "Apa nama kesultanan Islam pertama di Indonesia?", "jawaban": "samudera pasai"},
        {"pertanyaan": "Siapa penemu mesin cetak?", "jawaban": "johannes gutenberg"},
        {"pertanyaan": "Tahun berapa Tembok Berlin runtuh?", "jawaban": "1989"},
        {"pertanyaan": "Siapa pemimpin revolusi Kuba yang terkenal?", "jawaban": "fidel castro"},
        {"pertanyaan": "Siapa perdana menteri pertama India?", "jawaban": "jawaharlal nehru"},
        {"pertanyaan": "Apa nama perjanjian yang mengakhiri Perang Dunia I?", "jawaban": "perjanjian versailles"},
        {"pertanyaan": "Siapa penemu listrik?", "jawaban": "benjamin franklin"},
        {"pertanyaan": "Apa nama kapal Inggris yang tenggelam di Samudra Atlantik pada 1912?", "jawaban": "titanic"},
        {"pertanyaan": "Siapa pahlawan nasional Indonesia yang berasal dari Aceh?", "jawaban": "cut nyak dien"},
        {"pertanyaan": "Siapa kaisar Romawi yang memeluk agama Kristen?", "jawaban": "konstantinus"},
        {"pertanyaan": "Tahun berapa Perang Korea berakhir?", "jawaban": "1953"},
        {"pertanyaan": "Apa nama kesultanan terbesar di India?", "jawaban": "kesultanan mughal"},
        {"pertanyaan": "Siapa presiden Amerika Serikat yang terkena skandal Watergate?", "jawaban": "richard nixon"},
        {"pertanyaan": "Apa nama organisasi internasional yang didirikan setelah Perang Dunia II?", "jawaban": "perserikatan bangsa-bangsa"},
        {"pertanyaan": "Siapa tokoh terkenal dalam Perang Troya?", "jawaban": "achilles"},
        {"pertanyaan": "Apa nama perang sipil di Amerika Serikat?", "jawaban": "perang saudara"},
        {"pertanyaan": "Tahun berapa Napoleon Bonaparte wafat?", "jawaban": "1821"},
        {"pertanyaan": "Apa nama perjanjian yang mengakhiri Perang Dunia II?", "jawaban": "perjanjian san francisco"}
    ],
    "Matematika": [
        {"pertanyaan": "Berapakah hasil dari 5 + 7?", "jawaban": "12"},
        {"pertanyaan": "Berapakah hasil dari 9 x 9?", "jawaban": "81"},
        {"pertanyaan": "Berapakah akar kuadrat dari 64?", "jawaban": "8"},
        {"pertanyaan": "Berapakah hasil dari 7 - 3?", "jawaban": "4"},
        {"pertanyaan": "Berapakah hasil dari 11 x 11?", "jawaban": "121"},
        {"pertanyaan": "Berapakah hasil dari 15 / 3?", "jawaban": "5"},
        {"pertanyaan": "Berapakah hasil dari 25 - 17?", "jawaban": "8"},
        {"pertanyaan": "Berapakah hasil dari 8 x 7?", "jawaban": "56"},
        {"pertanyaan": "Berapakah hasil dari 9 + 6?", "jawaban": "15"},
        {"pertanyaan": "Berapakah hasil dari 36 / 6?", "jawaban": "6"},
        {"pertanyaan": "Berapakah hasil dari 49 + 49?", "jawaban": "98"},
        {"pertanyaan": "Berapakah hasil dari 144 : 12?", "jawaban": "12"},
        {"pertanyaan": "Berapakah hasil dari 50% dari 200?", "jawaban": "100"},
        {"pertanyaan": "Berapakah hasil dari 20 + 30?", "jawaban": "50"},
        {"pertanyaan": "Berapakah hasil dari 18 / 6?", "jawaban": "3"},
        {"pertanyaan": "Berapakah hasil dari 15 x 15?", "jawaban": "225"},
        {"pertanyaan": "Berapakah hasil dari 10 + 25?", "jawaban": "35"},
        {"pertanyaan": "Berapakah hasil dari 7 x 8?", "jawaban": "56"},
        {"pertanyaan": "Berapakah hasil dari 50 - 20?", "jawaban": "30"},
        {"pertanyaan": "Berapakah hasil dari 90 + 10?", "jawaban": "100"},
        {"pertanyaan": "Berapakah hasil dari 45 - 5?", "jawaban": "40"},
        {"pertanyaan": "Berapakah hasil dari 40 / 4?", "jawaban": "10"},
        {"pertanyaan": "Berapakah hasil dari 60 + 15?", "jawaban": "75"},
        {"pertanyaan": "Berapakah hasil dari 6 x 6?", "jawaban": "36"},
        {"pertanyaan": "Berapakah hasil dari 25 + 25?", "jawaban": "50"},
        {"pertanyaan": "Berapakah hasil dari 81 / 9?", "jawaban": "9"},
        {"pertanyaan": "Berapakah hasil dari 100 - 30?", "jawaban": "70"},
        {"pertanyaan": "Berapakah hasil dari 24 / 8?", "jawaban": "3"},
        {"pertanyaan": "Berapakah hasil dari 12 x 12?", "jawaban": "144"},
        {"pertanyaan": "Berapakah hasil dari 70 + 25?", "jawaban": "95"},
        {"pertanyaan": "Berapakah hasil dari 5 + 15?", "jawaban": "20"},
        {"pertanyaan": "Berapakah hasil dari 30 x 2?", "jawaban": "60"},
        {"pertanyaan": "Berapakah hasil dari 15 - 10?", "jawaban": "5"}
    ]
}

class QuizGame:
    def __init__(self, time_limit):
        self.window = tk.Tk()
        self.window.title("Quiz Game")
        self.window.geometry("500x400")
        self.window.configure(bg="#f0f0f0")
        
        self.score = 0
        self.current_question = None
        self.time_limit = time_limit * 60  # Total time in seconds
        self.start_time = 0
        
        # Add a title
        title_label = tk.Label(self.window, text="Selamat Datang di Quiz Game!", font=("Arial", 20, "bold"), bg="#f0f0f0", pady=10)
        title_label.pack()

        # Frame for Category and Question
        question_frame = tk.Frame(self.window, bg="#f0f0f0")
        question_frame.pack(pady=10)

        self.category_label = tk.Label(question_frame, text="", font=("Arial", 14), bg="#f0f0f0")
        self.category_label.pack()

        self.question_label = tk.Label(question_frame, text="", font=("Arial", 14), wraplength=450, bg="#f0f0f0")
        self.question_label.pack(pady=10)

        # Frame for Answer Entry
        answer_frame = tk.Frame(self.window, bg="#f0f0f0")
        answer_frame.pack(pady=10)

        answer_label = tk.Label(answer_frame, text="Masukkan Jawaban:", font=("Arial", 14), bg="#f0f0f0")
        answer_label.pack(side=tk.LEFT)

        self.answer_entry = tk.Entry(answer_frame, font=("Arial", 14), width=20)
        self.answer_entry.pack(side=tk.LEFT, padx=10)
        self.answer_entry.bind("<Return>", self.check_answer_event)

        # Button to submit answer
        self.submit_button = tk.Button(self.window, text="Submit", command=self.check_answer, font=("Arial", 14), bg="#4CAF50", fg="white")
        self.submit_button.pack(pady=10)

        # Frame for Score and Timer
        info_frame = tk.Frame(self.window, bg="#f0f0f0")
        info_frame.pack(pady=10)

        self.score_label = tk.Label(info_frame, text="Score: 0", font=("Arial", 14), bg="#f0f0f0")
        self.score_label.pack(side=tk.LEFT, padx=20)

        self.time_label = tk.Label(info_frame, text=f"Time remaining: {self.time_limit} seconds", font=("Arial", 14), bg="#f0f0f0")
        self.time_label.pack(side=tk.LEFT)

        self.feedback_label = tk.Label(self.window, text="", font=("Arial", 14), bg="#f0f0f0")
        self.feedback_label.pack(pady=10)

        self.update_timer()
        self.next_question()

        self.window.mainloop()

    def update_timer(self):
        if self.time_limit > 0:
            self.time_limit -= 1
            if self.time_limit <= 10:
                self.time_label.config(fg="red")  # Change to red when 10 seconds or less
            self.time_label.config(text=f"Time remaining: {self.time_limit} seconds")
            self.window.after(1000, self.update_timer)  # Update every 1 second
        else:
            messagebox.showinfo("Game Over", f"Waktu habis! Kamu berhasil menjawab {self.score} pertanyaan.")
            self.window.destroy()  # Close the game window when time is up

    def next_question(self):
        self.category_label.config(text="")
        self.question_label.config(text="")
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")

        category = random.choice(list(questions.keys()))
        question = random.choice(questions[category])

        self.category_label.config(text=f"Kategori: {category}")
        self.question_label.config(text=f"Pertanyaan: {question['pertanyaan']}")

        self.current_question = question
        self.start_time = time.time()

    def check_answer(self):
        user_answer = self.answer_entry.get().lower()

        if user_answer == self.current_question['jawaban'].lower():
            self.feedback_label.config(text="Benar!", fg="green")
            self.score += 1
        else:
            self.feedback_label.config(text=f"Salah! Jawaban yang benar adalah: {self.current_question['jawaban']}.", fg="red")

        self.score_label.config(text=f"Score: {self.score}")
        self.next_question()

    def check_answer_event(self, event):
        self.check_answer()

def start_game(time_limit, setup_window):
    setup_window.destroy()  # Close the setup window
    QuizGame(time_limit)

def main():
    window = tk.Tk()
    window.title("Pilih Waktu")
    window.geometry("300x200")
    window.configure(bg="#f0f0f0")

    time_limit_label = tk.Label(window, text="Pilih waktu limit (menit):", font=("Arial", 16), bg="#f0f0f0", pady=10)
    time_limit_label.pack()

    time_limit_var = tk.StringVar()
    time_limit_var.set("1")  # Default time is 1 minute

    time_limit_option = tk.OptionMenu(window, time_limit_var, "1", "2", "3")
    time_limit_option.config(font=("Arial", 14), bg="#4CAF50", fg="white")
    time_limit_option.pack(pady=10)

    start_button = tk.Button(window, text="Mulai", command=lambda: start_game(int(time_limit_var.get()), window), font=("Arial", 14), bg="#4CAF50", fg="white")
    start_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()