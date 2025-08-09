import os
import sys
import json
import pyaudio
import threading
from vosk import Model, KaldiRecognizer

# === 1. Setup model path ===
model_path = r"C:\Users\zbook\Downloads\Compressed\vosk-model-en-us-0.22\vosk-model-en-us-0.22"  # <-- Change this if needed

if not os.path.exists(model_path):
    print("Model folder not found. Please check the path!")
    sys.exit(1)

model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# === 2. Setup audio stream ===
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, 
                channels=1, 
                rate=16000, 
                input=True, 
                frames_per_buffer=8000)
stream.start_stream()

# === 3. Variables ===
full_text = ""  # Collected text

def listen_keyboard():
    """Separate thread to listen for Enter key."""
    global full_text
    while True:
        input("\n\n🔵 Press [ENTER] to finalize the sentence.\n")
        if full_text.strip():
            print(f"\n📝 Final Statement: {full_text.strip()}\n")
            full_text = ""  # Reset after printing
        else:
            print("\n⚪ Nothing to print yet.\n")

# === 4. Start listening to keyboard in background ===
keyboard_thread = threading.Thread(target=listen_keyboard, daemon=True)
keyboard_thread.start()

# === 5. Start microphone listening ===
print("🎙️ Start speaking. Press [ENTER] when you want to print it.")
try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            if text:
                full_text += " " + text
        else:
            partial = json.loads(recognizer.PartialResult()).get("partial", "")
            # (You can print live partials if you want)
except KeyboardInterrupt:
    print("\nProgram stopped by user.")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
