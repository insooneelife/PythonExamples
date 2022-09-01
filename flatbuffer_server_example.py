import sys
import socket
import flatbuffers
from flatbuffers import flexbuffers
import Packets.Body

header_size = 8
class MessageHeader(object):
    def __init__(self):
        self.type = 0
        self.size = 0

def send_packet(conn, bytes):
    type = 0
    size = len(bytes)

    typebytes = type.to_bytes(4, byteorder="little")
    sizebytes = size.to_bytes(4, byteorder="little")
    print("send  type:", type, " size:", size, " bytes:", bytes)

    b = bytearray()
    b.extend(typebytes)
    b.extend(sizebytes)
    b.extend(bytes)

    conn.send(b)  # send data to the client

def recv_packet(conn):
    data = conn.recv(8)
    if not data:
        print('not Data')
        return None

    header = MessageHeader()
    header.type = int.from_bytes(data[0:4], sys.byteorder)
    header.size = int.from_bytes(data[4:8], sys.byteorder)
    print("recv header  type:", header.type, " size:", header.size)

    body = conn.recv(header.size)
    print("recv body:", body)
    if not body:
        return None

    return body

def serialize(data):
    b = flatbuffers.Builder()
    str = b.CreateString(data)

    Packets.Body.BodyStart(b)
    Packets.Body.BodyAddData(b, str)
    body = Packets.Body.BodyEnd(b)
    b.Finish(body)
    print('serialize : ', b.Output())
    return b.Output()

def deserialize(body_bytes):
    body = Packets.Body.Body.GetRootAsBody(body_bytes)
    print("deserialize : ", body.Data())

def server_program():
    host = "127.0.0.1"
    port = 11000

    print('start')
    server_socket = socket.socket()
    server_socket.bind((host, port))

    while True:
        try:
            server_socket.listen(2)
            conn, address = server_socket.accept()
            print("Connection from: " + str(address))

            while True:
                body = recv_packet(conn)
                if body is None:
                    break

                deserialize(body)

                data = "this is data from server."
                bytes = serialize(data)
                print("serialized: ", bytes)
                send_packet(conn, bytes)

            print("close connection")
            conn.close()  # close the connection
        except socket.error:
            print(socket.error)

def test():
    data = "this is data from server."
    bytes = serialize(data)
    deserialize(bytes)

if __name__ == '__main__':
    server_program()
    #test()