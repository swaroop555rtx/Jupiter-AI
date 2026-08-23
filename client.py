import socket
import pyttsx3

from Action import execute_action


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak_offline(text):
    print(f"Assistant: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()




# ============================================================
# UNO Q CONNECTION
# ============================================================

UNO_Q_IP = "192.168.0.156"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting to UNO Q...")

client.connect((UNO_Q_IP, PORT))

print("Connected to UNO Q!")
speak_offline("Jupiter AI is connected to the UNO Q.")


# ============================================================
# MAIN LOOP
# ============================================================

print()
print("======================================")
print("       JUPITER AI TEST MODE")
print("======================================")
print("Type a command.")
print("Example: open chrome")
print("Type 'exit' to stop.")
print()


while True:

    try:

        # ----------------------------------------------------
        # TYPE COMMAND
        # ----------------------------------------------------

        command = input("You: ").strip()

        if not command:
            continue


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if command.lower() == "exit":

            client.sendall(b"exit")

            prediction = client.recv(4096).decode(
                "utf-8"
            ).strip()

            print("UNO Q:", prediction)

            speak_offline("Jupiter AI shutting down.")

            break


        # ----------------------------------------------------
        # SEND TEXT TO UNO Q
        # ----------------------------------------------------

        print("Sending to UNO Q...")

        client.sendall(
            command.encode("utf-8")
        )


        # ----------------------------------------------------
        # RECEIVE AI PREDICTION
        # ----------------------------------------------------

        prediction = client.recv(4096).decode(
            "utf-8"
        ).strip()

        print("UNO Q prediction:", prediction)


        # ----------------------------------------------------
        # EXECUTE ACTION
        # ----------------------------------------------------
        if prediction == "FUN_MODE":
            speak_offline("Which type of fun? YouTube, music or gaming?")
            fun_choice = input("You: ").strip().lower()
            if "youtube" in fun_choice:        # indented one more level!
                execute_action("OPEN_YOUTUBE", speak_offline, None, None)
            elif "music" in fun_choice:
                 execute_action("OPEN_MUSIC", speak_offline, None, None)
            elif "game" in fun_choice or "roblox" in fun_choice:
                execute_action("OPEN_ROBLOX", speak_offline, None, None)


        elif prediction == "PC_SHUTDOWN":
            speak_offline("Are you sure? Type yes or no.")
            confirm = input("You: ").strip().lower()
            if confirm in {"yes", "yeah"}:
                execute_action("PC_SHUTDOWN_CONFIRMED", speak_offline, None, None)
            else:
                speak_offline("Shutdown cancelled.")

        else:
            execute_action(prediction, speak_offline, None, None)

        


        print("💤 Ready for next command.")
        print()


    except KeyboardInterrupt:

        print("\nJupiter AI stopped.")
        break


    except Exception as error:

        print("Error:", error)
        print("Returning to command mode...")


# ============================================================
# CLEANUP
# ============================================================

client.close()

print("Connection closed.")