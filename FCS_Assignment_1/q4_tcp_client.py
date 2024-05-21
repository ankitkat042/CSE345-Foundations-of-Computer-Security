import sys
import socket
import hashlib

def compute_sha256(data):
    hash_object = hashlib.sha256(data.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig

def client_program():
    server_ip = "127.0.0.1"
    server_port = 12345

    try:
        print("Client: Creating socket...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print(f"Client: Connecting to {server_ip}:{server_port}...")
        s.connect((server_ip, server_port))

        message = input("Enter the message to send: ")
        hash_value = compute_sha256(message)
        combined_message = message + "|" + hash_value

        print("Client: Sending message to server...")
        s.sendall(combined_message.encode())

        print("Client: Waiting for response...")
        response = s.recv(1024).decode()
        if response == "Message Verified":
            print("Hello Client, Server has verified the integrity of the message.")
        elif response == "Message Tampered":
            print("Server detected tampering with the message.")
        else:
            print("Unexpected response from server.")

        flag = input("Do you want to send another message? (y/n): ")
        if flag.lower() == "y":
            client_program()
        else:
            print("Exiting client...")
            s.close()
            sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    mode = input("Choose role (server/client): ")
    if mode == "client":
        client_program()
    else:
        print("Invalid role selected. Exiting.")
