import pickle
import socket
from datetime import datetime

class RecordData:
    def __init__(self, start = False, name = "", time = "", version = ""):
        self.start = start
        self.name = name
        self.time = time
        self.version = version

    def __str__(self):
        return f"Start: {self.start}, Name: {self.name}, Time: {self.time}, Version: {self.version}"

def send_start_to_record_server():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = 12345
        client_socket.connect((host, port))
        now = datetime.now()
        datetime_string = now.strftime("%Y-%m-%d %H:%M:%S")
        senddata = RecordData(True, "blabla", datetime_string, "1.1.0")

        client_socket.send(pickle.dumps(senddata))
        data = client_socket.recv(1024)

        recvdata = pickle.loads(data)
        print(f"recv from record server: {recvdata}")
        
        client_socket.close()
    except socket.error as e:
        print(f"cannot connect to record server: {e}")



if __name__ == '__main__':
    send_start_to_record_server()
