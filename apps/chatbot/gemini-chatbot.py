import google.generativeai as genai
import sys

# Optional: color output if installed
try:
    from colorama import init, Fore, Style
    init()
    GREEN = Fore.GREEN
    BLUE = Fore.CYAN
    RESET = Style.RESET_ALL
except:
    GREEN = BLUE = RESET = ""

# Configure API
API_KEY = "AIzaSyBLD3eDvxpMWlI0Rql4g5Ax-JV0U_HyMyM"  # ← Replace with your Gemini API key
genai.configure(api_key=API_KEY)

# Initialize chat
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

print(f"{BLUE}Gemini Terminal Chat ✨ — Type 'exit' to quit.{RESET}\n")

while True:
    try:
        prompt = input(f"{GREEN}You:{RESET} ").strip()
        if prompt.lower() in ["exit", "quit"]:
            print(f"{BLUE}Goodbye! 👋{RESET}")
            break
        if not prompt:
            continue

        response = chat.send_message(prompt)
        reply = response.text.strip()

        print(f"\n{BLUE}Gemini:{RESET}\n{reply}\n")

    except KeyboardInterrupt:
        print("\n\nKeyboard interrupt. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}⚠️ Error: {e}{RESET}\n")
