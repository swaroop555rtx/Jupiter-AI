import os
import time
import shutil
import subprocess
from pathlib import Path

import speech_recognition as sr


def open_program(program_path, speak_offline, name):
    """Open an application safely and report errors."""
    try:
        if not os.path.exists(program_path):
            speak_offline(f"I could not find {name}.")
            print(f"{name} not found: {program_path}")
            return

        speak_offline(f"Opening {name}.")
        subprocess.Popen([program_path])

    except Exception as error:
        print(f"Could not open {name}: {error}")
        speak_offline(f"Sorry, I could not open {name}.")


def OPEN_CHROME(speak_offline):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    open_program(chrome_path, speak_offline, "Chrome")


def STUDY_MODE(speak_offline):
    speak_offline("Opening Notepad for study mode.")
    subprocess.Popen(["notepad.exe"])


def CODE_MODE(speak_offline):
    possible_paths = [
        r"C:\Users\Admin\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        r"C:\Program Files\Microsoft VS Code\Code.exe",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            open_program(path, speak_offline, "Visual Studio Code")
            return

    # Works if VS Code's `code` command is installed in PATH.
    if shutil.which("code"):
        speak_offline("Opening Visual Studio Code.")
        subprocess.Popen(["code"])
        return

    speak_offline("I could not find Visual Studio Code.")



def FUN_MODE(speak_offline, recognizer, transcribe_audio):
    
    
    speak_offline("Which type of fun do you want? YouTube, music, or gaming?")
    time.sleep(0.4)

    try:
        with sr.Microphone() as source:
            print("Listening for fun option...")
            recognizer.adjust_for_ambient_noise(source, duration=0.7)

            audio_data = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=5
            )

        fun = transcribe_audio(audio_data).lower().strip()
        print(f"Fun option: {fun}")

        if not fun:
            speak_offline("Sorry, I could not hear a command.")
            return

        if "youtube" in fun:
            speak_offline("Opening YouTube.")
            return "OPEN_YOUTUBE"

        elif "music" in fun:
            speak_offline("Opening YouTube Music.")
            return "OPEN_YTMUSIC"

        elif "game" in fun or "gaming" in fun or "roblox" in fun:
            speak_offline("Opening Roblox.")  # add this!
            return "OPEN_ROBLOX"

        else:
            speak_offline("I did not recognize that option.")

    except sr.WaitTimeoutError:
        speak_offline("I did not hear an option.")

    except Exception as error:
        print(f"Fun mode error: {error}")
        speak_offline("Sorry, I could not process that option.")


def PC_SHUTDOWN(speak_offline, recognizer, transcribe_audio):
    """Ask for a spoken confirmation before shutting down Windows."""
    speak_offline("Are you sure you want to shut down the computer? Say yes or no.")
    time.sleep(0.4)

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.7)

            audio_data = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=4
            )

        answer = transcribe_audio(audio_data).lower().strip()
        print(f"Shutdown confirmation: {answer}")

        if answer in {"yes", "yeah", "confirm", "shutdown", "shut down"}:
            speak_offline("Shutting down the computer in ten seconds.")
            return "PC_SHUTDOWN_CONFIRM"

        else:
            speak_offline("Shutdown cancelled.")

    except sr.WaitTimeoutError:
        speak_offline("No confirmation received. Shutdown cancelled.")

    except Exception as error:
        print(f"Shutdown error: {error}")
        speak_offline("I could not complete the shutdown request.")


# These functions need smart-light or hardware integration later.



def execute_action(prediction, speak_offline, recognizer, transcribe_audio):
    """Run the function that matches the predicted dataset intent."""

    if prediction == "OPEN_CHROME":
        OPEN_CHROME(speak_offline)

    elif prediction == "CODE_MODE":
        CODE_MODE(speak_offline)

    elif prediction == "STUDY_MODE":
        STUDY_MODE(speak_offline)

    elif prediction == "FUN_MODE":
        FUN_MODE(speak_offline, recognizer, transcribe_audio)


    elif prediction == "PC_SHUTDOWN":
        PC_SHUTDOWN(speak_offline, recognizer, transcribe_audio)

    elif prediction == "OPEN_YOUTUBE":
        speak_offline("Opening YouTube.")
        subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "https://www.youtube.com"])

    elif prediction == "OPEN_MUSIC":
        speak_offline("Opening YouTube Music.")
        subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "https://music.youtube.com"])

    elif prediction == "OPEN_ROBLOX":
        speak_offline("Opening Roblox.")
        os.startfile("roblox://")

    elif prediction == "PC_SHUTDOWN_CONFIRMED":
        os.system("shutdown /s /t 10")



    else:
        print(f"Unknown prediction: {prediction}")
        speak_offline("Sorry, I do not know how to perform that action.")