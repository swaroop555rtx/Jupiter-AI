Jupiter AI 🪐

An on-device AI-powered desktop assistant built on the Arduino UNO Q. Jupiter AI understands natural language commands and controls your PC in real time — no cloud, no internet dependency.

🧠 How It Works
User Command (text/voice)
        ↓
  Laptop captures input
        ↓
  Sends text to Arduino UNO Q via WiFi
        ↓
  UNO Q runs Whisper + Naive Bayes intent classifier
        ↓
  Sends prediction back to Laptop
        ↓
  Laptop executes action
⚡ Features
Wake word detection — "Jupiter AI"
Natural language intent classification
Opens Chrome, VS Code, Notepad
YouTube, YouTube Music, Roblox launcher
PC shutdown with confirmation
Smart LED control (WS2812B) — coming soon
Fully offline AI processing on UNO Q
🔧 Hardware
Arduino UNO Q (MPU + MCU)
WS2812B LED Strip (future version)
300-ohm resistor
5V power adapter
📁 Project Structure
JupiterAI/
├── predict.py     # Runs on UNO Q — intent classification server
├── client.py      # Runs on Laptop — input handling + action execution
├── Action.py      # Action functions (open apps, shutdown, etc.)
├── model.pkl      # Trained Naive Bayes intent model
└── vectorizer.pkl # TF-IDF vectorizer
🚀 How To Run

1. On Arduino UNO Q:

bash
python3 predict.py

2. On Laptop:

bash
python client.py
🛠️ Tech Stack
Python 3
Faster-Whisper (tiny.en)
Scikit-learn (Naive Bayes)
Socket (WiFi communication)
pyttsx3 (text to speech)
SpeechRecognition + PyAudio
🔮 Future Improvements
WS2812B smart LED control via STM32 MCU
Custom wake word model for lower power consumption
More PC actions and app integrations
Bluetooth audio support on Linux
📋 Requirements
bash
pip install faster-whisper scikit-learn speechrecognition pyaudio pyttsx3 joblib

Built for Arduino Challenge — powered by Arduino UNO Q 🪐

NOTE
AI tools were used for code assistance and documentation during the development of this project.
