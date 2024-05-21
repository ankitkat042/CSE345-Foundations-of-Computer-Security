import sys
import socket
import hashlib

def compute_sha256(data):
    hash_object = hashlib.sha256(data.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig

def client(server_ip, server_port):
    try:
        print("Client: Creating socket...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print(f"Client: Connecting to {server_ip}:{server_port}...")
        s.connect((server_ip, server_port))
        
        message = "Hello, Server!"
        hash_value = compute_sha256(message)
        combined_message = message + "|" + hash_value
        
        print("Client: Sending message to server...")
        s.sendall(combined_message.encode())
        
        print("Client: Waiting for response...")
        response = s.recv(1024).decode()
        if response == "Hello, Client!":
            print(response)
        elif response == "Message Verified":
            print("Server has verified the integrity of the message.")
        elif response == "Message Tampered":
            print("Server detected tampering with the message.")
        else:
            print("Unexpected response from server.")
        
        flag =  input("Do you want to send another message? (y/n): ")
        if flag == "y":
            client(server_ip, server_port)
        else:
            print("Exiting client...")
            s.close()
            sys.exit(0)

    except Exception as e:
        print(f"Error: {e}")

def server(listen_ip, listen_port):
    print("Server: Creating socket...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print(f"Server: Binding to {listen_ip}:{listen_port}...")
    s.bind((listen_ip, listen_port))
    
    print(f"Server: Listening for connections...")
    s.listen(1)
    
    print(f"Server: Accepting a connection...")
    conn, addr = s.accept()
    
    print(f"Server: Received connection from {addr}...")
    data = conn.recv(1024).decode()
    message, received_hash = data.split('|')
    
    print("Server: Processing received message...")
    computed_hash = compute_sha256(message)
    if computed_hash == received_hash:
        conn.sendall("Message Verified".encode())
        print("Client has verified the integrity of the message: ", message)
    else:
        conn.sendall("Message Tampered".encode())
        print("Mismatch in message integrity detected!")

    flag =  input("Do you want to receive another message? (y/n): ")
    if flag == "y":
        server(listen_ip, listen_port)
    else:
        print("Exiting server...")
        s.close()
        sys.exit(0)


def answer3(mode):
    if mode == "server":
        server("127.0.0.1", 8080)
    elif mode == "client":
        client("127.0.0.1", 8080)
    else:
        print("Invalid mode. Use 'server' or 'client'.")

def client_send_1(send_message,server_ip, server_port):
    try:
        print("Client: Creating socket...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print(f"Client: Connecting to {server_ip}:{server_port}...")
        s.connect((server_ip, server_port))
        
        message = send_message
        
        print("Client: Sending message to server...")
        s.sendall(message.encode())
        
        print("Client: Waiting for response...")
        response = s.recv(1024).decode()
        if response == "Hello, Client!":
            print(response)
        elif response == "Message Verified":
            print("Server has verified the integrity of the message.")
        else:
            print("Unexpected response from server.")

    except Exception as e:
        print(f"Error: {e}")



def server_receive_1(receive_message,listen_ip, listen_port):
    print("Server: Creating socket...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print(f"Server: Binding to {listen_ip}:{listen_port}...")
    s.bind((listen_ip, listen_port))
    
    print(f"Server: Listening for connections...")
    s.listen(1)
    
    print(f"Server: Accepting a connection...")
    conn, addr = s.accept()
    
    print(f"Server: Received connection from {addr}...")
    data = conn.recv(1024).decode()
    message = "Hello, Client!"
    
    print("Server: Processing received message...")
    if message == receive_message:
        conn.sendall("Message Verified".encode())
        print("Client has verified the integrity of the message: ", message)
    else:
        conn.sendall("Message Tampered".encode())
        print("Mismatch in message integrity detected!")

def answer1():
    send_message = input("Enter the message to be sent: ")
    client_send_1(send_message,"127.0.0.1", 8080)

def answer2():
    receive_message = input("Enter the message to be received: ")
    server_receive_1(receive_message,"127.0.0.1", 8080)
