import time
import requests
import pyttsx3
import pyperclip

API = "http://127.0.0.1:8000/check_link"

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

last_text = ""

print("Background link scanner running...")

while True:
    try:
        text = pyperclip.paste()

        if text != last_text:
            last_text = text

            if text.startswith("http"):
                try:
                    response = requests.post(API, json={"link": text})
                    data = response.json()

                    if data.get("scam"):
                        print("⚠️ Scam link detected!")
                        speak("Warning! Suspicious link detected")
                    else:
                        print("✅ Link looks safe")
                except Exception as e:
                    print("Error calling API:", e)

    except Exception as e:
        print("Error reading clipboard:", e)

    time.sleep(2)