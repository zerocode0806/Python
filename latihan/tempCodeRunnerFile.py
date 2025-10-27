import os
import subprocess

# Use correct app path or shell method
def open_whatsapp():
    try:
        # Store version
        # subprocess.Popen("shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App", shell=True)
        
        # Or standalone version:
        subprocess.Popen([r"C:\Users\ADVAN\AppData\Local\WhatsApp\WhatsApp.exe"])
    except Exception as e:
        print(f"Gagal membuka WhatsApp: {e}")
