'''
Created on Jul 3, 2018
@author: ThiefOfTime (m_lenk@gmx.de)
'''

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import re
import time
import sys

from abstract import AbstractClient


class Client(AbstractClient):

    def __init__(self):
        super(Client, self).__init__()
        # ask for server address and client port
        self.server_addr = str(input('Enter Host IP-Address:  '))
        # check if the ip addr is in the right format
        if self.server_addr == '\n' or len(self.server_addr.strip()) == 0 \
                or not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',self.server_addr.strip()):
            self.server_addr = '127.0.0.1'
        self.name = input('Please enter your name:  ')
        self.users = {}
        self.connections = {}
        try:
            # try to connect to the server
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((self.server_addr, self.server_port))
            self.socket.send(bytes(self.name, 'utf8'))
            self.receive_thread = Thread(target=self.recive_server_messages)
            self.receive_thread.start()
        except Exception:
            print('The connection to the server could not be established')

    def recive_server_messages(self):
        while True:
            try:
                # get the next user message
                msg = str(self.socket.recv(1024).decode("utf8"))
                if len(msg) > 0:
                    # skip empty messages
                    if msg.startswith('#list'):
                        # if server sends the client list, print it neatly
                        msg = msg.split(' ', 1)[1].split(';')
                        msg.remove(self.name)
                        self.users = msg
                        self.print_client_list()
                    else:
                        # print the message as it comes
                        print(msg)
            except Exception:
                break

    def run(self):
        while True:
            try:
                # get the new user input
                msg = input('')
                self.socket.send(bytes(msg, 'utf8'))
                if msg == '#quit':
                    # if quit, contact server and close connections
                    break
            except Exception:
                print('Server is down')
        # clean up after yourself
        self.socket.close()
        sys.exit(1)


if __name__ == "__main__":
    client = Client()
    client.run()

