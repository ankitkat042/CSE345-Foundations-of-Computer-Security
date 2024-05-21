import sys
import socket
import hashlib

def compute_sha256(data):
    hash_object = hashlib.sha256(data.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig

def server_program():
    listen_ip = "127.0.0.1"
    listen_port = 12345

    print("Server: Creating socket...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #reuse of the address
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"Server: Binding to {listen_ip}:{listen_port}...")
    try:
        s.bind((listen_ip, listen_port))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    s.listen(1)
    print(f"Server: Listening for connections...")
    while True:
        print(f"Server: Accepting a connection...")
        conn, addr = s.accept()

        print(f"Server: Received connection from {addr}...")
        data = conn.recv(1024).decode()
        message, received_hash = data.split('|')

        print("Server: Processing received message...")
        computed_hash = compute_sha256(message)
        if computed_hash == received_hash:
            conn.sendall("Message Verified".encode())
            print("Client has verified the integrity of the message:", message)
        else:
            conn.sendall("Message Tampered".encode())
            print("Mismatch in message integrity detected!")

        conn.close()

        flag = input("Do you want to receive another message? (y/n): ")
        if flag.lower() != "y":
            break
    print("Exiting server...")
    s.close()
    sys.exit(0)


if __name__ == "__main__":
    mode = input("Choose role (server/client): ")
    if mode == "server":
        server_program()
    else:
        print("Invalid role selected. Exiting.")
