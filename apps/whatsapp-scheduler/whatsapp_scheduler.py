from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

# Konfigurasi WebDriver
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:/Users/ADVAN/AppData/Local/Google/Chrome/User Data")  # Ganti dengan path yang sesuai
chrome_options.add_argument("--profile-directory=Default")  # Profil default
service = Service('C:/Users/ADVAN/Downloads/chromedriver.exe')  # Path ke chromedriver  # Path ke chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Buka WhatsApp Web
driver.get('https://web.whatsapp.com/')

# Tunggu hingga pengguna login
print("Silakan login ke WhatsApp Web dan tekan Enter setelah login.")
input("Tekan Enter setelah login...")

def send_whatsapp_message(phone_number, message):
    # Temukan field pencarian untuk nomor telepon
    search_box = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.send_keys(phone_number)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)  # Tunggu hingga chat terbuka

    # Temukan field input pesan
    message_box = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="6"]')
    message_box.click()
    message_box.send_keys(message)
    message_box.send_keys(Keys.ENTER)
    print(f"Pesan dikirim ke {phone_number}")

phone_number = "+6288298697330"
message = "Ini adalah pesan otomatis yang dikirim setiap 20 detik!"

while True:
    send_whatsapp_message(phone_number, message)
    time.sleep(20)  # Tunggu 20 detik sebelum mengirim pesan lagi
