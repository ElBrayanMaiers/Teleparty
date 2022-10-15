
import socket
import base64

code = base64.b64encode(b"""
class Listen():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(2000)

    def ReadData(self):
        return self.client.recv(1024).decode("utf-8")

    def Join(self, ip, name):
        try:
            self.client.connect((ip, 80))
            self.client.sendall(("Nm"+str(name)).encode("utf-8"))
            # while True:
            #     pass
            # return True
        except:
            return False

    def PairedServer(self, ip):
        self.client.sendall("Connected Succesfully".encode("utf-8"))
Listen()""")

exec(base64.b64decode(code))