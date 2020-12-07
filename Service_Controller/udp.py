import socket
import time

class UDPServer():
    # Configuração do Servidor
    server_ip = "127.0.0.1"
    server_port = 27000
    client_ip = "127.0.0.1"
    client_port = 27001
    buffer_size = 1024
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def __init__(self,server_ip :str, server_port :int , client_ip :int, client_port :int, buffer_size :int):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_ip = client_ip
        self.client_port = client_port
        self.buffer_size = buffer_size
        self.sock.bind((self.server_ip, self.server_port))

    def send_message(self, msg :str):
        send_bytes = str.encode(msg)
        self.sock.sendto(send_bytes,(self.client_ip,self.client_port))
    
    def receive_message(self):
        data = self.sock.recv(self.buffer_size)
        return data
    
class UDPclient():
    # Configuração do Servidor
    server_ip = "127.0.0.1"
    server_port = 27000
    buffer_size = 1024
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def __init__(self,server_ip :str, server_port :int , buffer_size :int):
        self.server_ip = server_ip
        self.server_port = server_port
        self.buffer_size = buffer_size

    def send_message(self, msg :str):
        send_bytes = str.encode(msg)
        self.sock.sendto(send_bytes,(self.server_ip,self.server_port))
    
    def receive_message(self, timeout :int):
        try:
            self.sock.settimeout(timeout)
            data = self.sock.recv(self.buffer_size)
            data = data.decode('utf-8')
            return data
        except:
            return None
        