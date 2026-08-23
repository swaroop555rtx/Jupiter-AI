import socket
import joblib

HOST = "0.0.0.0"
PORT = 5000

# Load AI model
intent_model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

print("Jupiter AI model loaded!")
print("Waiting for laptop...")

# Create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print(f"Listening on port {PORT}...")

while True:
    conn, addr = server.accept()

    print(f"Laptop connected: {addr}")

    try:
        while True:
            # Receive text from laptop
            data = conn.recv(4096)

            if not data:
                print("Laptop disconnected.")
                break

            command = data.decode("utf-8").strip()

            print(f"Received: {command}")

            # Exit
            if command.lower() == "exit":
                conn.sendall(b"EXIT")
                break

            # AI prediction
            user_input_vectorized = vectorizer.transform([command])
            prediction = intent_model.predict(user_input_vectorized)[0]

            print(f"Prediction: {prediction}")

            # Send prediction back to laptop
            conn.sendall(prediction.encode("utf-8"))

    except Exception as error:
        print(f"Connection error: {error}")

    finally:
        conn.close()
        print("Waiting for laptop...")
