import time
import requests
import pyperclip
import pyttsx3
from plyer import notification

# Your deployed API
API = "https://shield-india-api.onrender.com/check_link"

# voice engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

last_text = ""

print("🛡 Shield India Background Link Scanner Running...")

while True:
    try:
        text = pyperclip.paste()

        if text != last_text:
            last_text = text

            if text.startswith("http"):

                response = requests.post(API, json={"link": text})
                data = response.json()

                if data.get("scam"):

                    print("⚠️ Scam link detected!")

                    notification.notify(
                        title="⚠️ Shield India Alert",
                        message="Suspicious link detected! Do NOT open this link.",
                        timeout=6
                    )

                    speak("Warning. Suspicious link detected. Do not open it.")

                else:

                    print("✅ Link looks safe")

                    notification.notify(
                        title="Shield India",
                        message="Link looks safe.",
                        timeout=4
                    )

    except Exception as e:
        print("Error:", e)

    time.sleep(2)