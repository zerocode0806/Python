import os
import re

def load_qa(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    qa_dict = {}
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                if '|' in line:
                    question, answer = line.strip().split('|', 1)
                    qa_dict[question.lower()] = answer
    return qa_dict

def save_qa(filename, question, answer):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'a', encoding='utf-8') as file:
        file.write(f"{question}|{answer}\n")

def save_history(user_input, response):
    with open("history.txt", 'a', encoding='utf-8') as file:
        file.write(f"User: {user_input}\nBot: {response}\n")

def evaluate_math(question):
    question = question.lower()

    # Ganti kata operasi ke simbol
    question = question.replace("tambah", "+").replace("ditambah", "+")
    question = question.replace("kurang", "-").replace("dikurang", "-")
    question = question.replace("kali", "*").replace("dikali", "*")
    question = question.replace("bagi", "/").replace("dibagi", "/")

    # Cari pola angka dan operasi
    match = re.search(r'([\d\.]+)\s*([\+\-\*/])\s*([\d\.]+)', question)
    if match:
        try:
            num1 = float(match.group(1))
            operator = match.group(2)
            num2 = float(match.group(3))
            result = eval(f"{num1} {operator} {num2}")
            return f"Hasilnya adalah {result}"
        except:
            return "Maaf, saya tidak bisa menghitung itu."
    return None

def chatbot():
    qa_dict = load_qa("qa.txt")
    print("Halo! Saya Chatbot Self-Learning. Ketik 'keluar' untuk berhenti.\n")

    while True:
        user_input = input("Kamu: ").strip().lower()

        if user_input == 'keluar':
            print("Chatbot: Sampai jumpa!")
            break

        # 1. Cek apakah pertanyaan sudah ada di qa.txt
        if user_input in qa_dict:
            response = qa_dict[user_input]

        # 2. Cek apakah pertanyaan adalah soal matematika
        else:
            math_result = evaluate_math(user_input)
            if math_result:
                response = math_result

            # 3. Jika tidak ada di data & bukan soal matematika → tambahkan ke qa.txt
            else:
                response = input("Chatbot: Saya belum tahu jawabannya. Apa jawaban yang benar? ")
                save_qa("qa.txt", user_input, response)
                qa_dict[user_input] = response

        print(f"Chatbot: {response}")
        save_history(user_input, response)

chatbot()
