import socket
import sys
import threading
import server as ser
import select


class Proxy:
    def __init__(self, port):
        self.flag = False
        self.input_list = set()
        self.connections = {}
        self.for_del = []
        self.port = port

    def process(self):
        print("Waiting for connect")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', int(self.port)))
            s.listen(200)
            self.input_list.add(s)
        except Exception as e:
            sys.exit(e)

        while True:
            try:
                inputs, _, _ = select.select(self.input_list, [], [])
                for sock in inputs:
                    if sock == s:
                        client, addr = s.accept()
                        data = self.receive(client)
                        threading.Thread(target=ser.Server.handle_request,
                                         args=(
                                             client, data, self
                                         )).start()
                    else:
                        data = self.receive(sock)
                        if not data:
                            self.for_del.append(sock)
                        else:
                            self.connections[sock].send(data)
            except ConnectionResetError:
                client.close()
            try:
                for _s in self.for_del:
                    if _s == s:
                        continue
                    _s.close()
                    self.input_list.remove(_s)
                    if self.connections[_s] in self.input_list:
                        self.input_list.remove(self.connections[_s])
                    del self.connections[_s]
            except:
                pass

    @staticmethod
    def receive(s):
        s.settimeout(1)
        try:
            data = b''
            while True:
                part = s.recv(8192)
                if not part:
                    return data
                data += part
        finally:
            return data
