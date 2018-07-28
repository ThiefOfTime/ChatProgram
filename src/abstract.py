'''
Created on Jul 3, 2018
@author: ThiefOfTime (m_lenk@gmx.de)
'''

from abc import ABCMeta, abstractmethod


class AbstractClient:

    __metaclass__ = ABCMeta

    def __init__(self):
        '''

        :param addr: client address
        :param cport: port of the client
        '''
        self.addr = ''
        self.port = ''
        self.server = None
        self.users = []

    @abstractmethod
    def recive_messages(self):
        raise NotImplementedError()

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    @abstractmethod
    def recive_server_messages(self):
        raise NotImplementedError()

    def print_client_list(self):
        # print user list
        for user in self.users:
            print('<user> %s' %user)


class AbstractServer:

    __metaclass__ = ABCMeta

    def __init__(self, cport):
        '''

        :param cport: port of the client
        '''
        self.port = cport
        self.client_list = {}
        self.name_ip_client_list = {}
        self.clients = {}

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    @abstractmethod
    def serve_client(self, client, client_addr):
        raise NotImplementedError()

    @abstractmethod
    def listen(self, num_clients):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    def remove_client(self, name):
        for key in self.client_list.keys():
            if self.name_ip_client_list[name][0] in key:
                del self.client_list[key]
                break
        del self.name_ip_client_list[name]
        del self.clients[name]