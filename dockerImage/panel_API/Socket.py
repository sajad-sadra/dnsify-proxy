import socket
PORT = 8585
HOST = '0.0.0.0'

class ServerSocket:
    def __init__(self):
        self.serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((HOST, PORT))
        print("......start listenning at port " + str(PORT))
        self.serversocket.listen(1)
        (clientsocket, address) = self.serversocket.accept()
        print("+++++ Client Connect +++++")
        self.client = clientsocket

    def send(self,message):
        try:
            self.client.send(str(message).encode())
        except:
            print("!!! --EROR-- !!!")
            self.stopCon()

    def recive(self):
        ans = ""
        try:
            ans = self.client.recv(1024).decode()
        except:
            ans = "{error}"
            print("!!! ++EROR++ !!!")
        return ans

    def stopCon(self):
        try:
            self.client.shutdown(1)
            self.serversocket.shutdown(1)
        except:
            print("EROR IN SHUTing SOCKET")
        self.serversocket.close()
        self.client.close()

