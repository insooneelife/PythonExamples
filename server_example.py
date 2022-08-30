import sys
import socket

header_size = 8
class MessageHeader(object):
    def __init__(self):
        self.type = 0
        self.size = 0

def send_packet(conn, textdata):
    sbytes = bytearray(map(ord, textdata))
    type = 0
    size = len(sbytes)

    typebytes = type.to_bytes(4, byteorder="little")
    sizebytes = size.to_bytes(4, byteorder="little")
    print("send type:", type, " size:", size, " data:", textdata)

    b = bytearray()
    b.extend(typebytes)
    b.extend(sizebytes)
    b.extend(sbytes)

    conn.send(b)

def recv_packet(conn):
    data = conn.recv(8)
    if not data:
        print("not Data")
        return None

    header = MessageHeader()
    header.type = int.from_bytes(data[0:4], sys.byteorder)
    header.size = int.from_bytes(data[4:8], sys.byteorder)
    print("recv header type:", header.type, " size:", header.size)

    body = conn.recv(header.size)
    print("recv body:", body)
    if not body:
        return None

    return body

def server_program():
    host = "127.0.0.1"
    port = 11000

    server_socket = socket.socket()
    server_socket.bind((host, port))

    while True:
        try:
            server_socket.listen(2)
            conn, address = server_socket.accept()
            print("Connection from:", str(address))

            while True:
                body = recv_packet(conn)
                if body is None:
                    break
                print("from connected user:", str(body))
                send_packet(conn, "this is data from server.")
                print("close connection")
        except socket.error:
            print(socket.error)
            conn.close()

if __name__ == '__main__':
    server_program()