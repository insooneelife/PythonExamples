import pickle
import socket
import json
from datetime import datetime

class RecordData:
    def __init__(self, start = False, name = "", time = "", version = ""):
        self.start = start
        self.name = name
        self.time = time
        self.version = version

    def __str__(self):
        return f"Start: {self.start}, Name: {self.name}, Time: {self.time}, Version: {self.version}"

def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    
    server_socket.bind((host, port))
    
    server_socket.listen(5)
    print(f"서버가 {host}:{port} 에서 대기 중입니다.")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"{addr} 에서 연결되었습니다.")
        
        data = client_socket.recv(1024)

        recvdata = pickle.loads(data)

        print(f"클라이언트로부터 받은 메시지: {recvdata}")

        senddata = pickle.dumps(recvdata)
        client_socket.send(senddata)
        client_socket.close()

if __name__ == '__main__':
    start_server()

