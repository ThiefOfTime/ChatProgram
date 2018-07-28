'''
Created on Jul 3, 2018
@author: ThiefOfTime (m_lenk@gmx.de)
'''

from threading import Thread
import sys
import bluetooth
import uuid

from abstract import AbstractServer


class Server(AbstractServer):

    def __init__(self, port=1337):
        super(Server, self).__init__(cport=port)
        addr = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
        addr = 'b8:27:eb:53:AD:07'
        # create the Socket and bind to the address
        port = 1
        self.server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server.bind((addr, port))
        print('[MAC Adress] %s' % addr)

    def run(self):
        try:
            while True:
                # listen for client connections
                client, client_address = self.server.accept()
                # save the connection (unique)
                self.client_list[client_address] = client
                # start searving thread
                Thread(target=self.serve_client, args=(client, client_address)).start()
        except:
            self.server.close()

    def serve_client(self, client, client_addr):
        # if client connects, send greetings
        name = str(client.recv(1024).decode('utf8'))
        greeting = '<server> Welcome %s! If you ever want to quit, type #quit to exit.' % name
        print(greeting)
        client.send(bytes(greeting, 'utf8'))
        self.name_ip_client_list[name] = client_addr
        self.clients[name] = client
        while True:
            message = client.recv(1024)
            if message == bytes('#list', 'utf8'):
                # create list and send it to client, client needs different ports
                ret = ';'.join(self.name_ip_client_list.keys())
                ret = '#list %s'%ret
                client.send(bytes(ret, 'utf8'))
            elif str(message.decode('utf8')).startswith('@'):
                # if message starts with @ it has to be forwarded
                msg = str(message.decode('utf8'))
                if msg.startswith('@echo'):
                    # send message back to the client
                    message = str(message.decode('utf8')).rsplit(' ', 1)[1]
                    client.send(bytes('<server> %s'%message, 'utf8'))
                else:
                    try:
                        # send the message to the specified user
                        n_name, msg = msg.split(' ', 1)
                        n_name = n_name[1:]
                        if n_name in self.clients.keys():
                            n_client = self.clients[n_name]
                            n_client.send(bytes('<%s> %s' % (name, msg), 'utf8'))
                    except Exception:
                        client.send(bytes('The user %s is not online anymore' % n_name))
            elif str(message.decode('utf8')) == '#quit':
                # close the connection and forget the client
                client.close()
                self.remove_client(name)
                break
            else:
                pass

    def listen(self, num_clients):
        # define the number of clients that is being allowed
        self.server.listen(num_clients)

    def close(self):
        # close the server
        self.server.close()


if __name__ == "__main__":
    serv = Server()
    serv.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    accept_thread = Thread(target=serv.run)
    accept_thread.start()
    accept_thread.join()
    serv.close()
    sys.exit(1)
