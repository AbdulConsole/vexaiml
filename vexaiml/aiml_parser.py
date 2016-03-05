from __future__ import print_function
import os
from os import path

import aiml
import zmq


class AIMLParser:
    def __init__(self,
                 context=None,
                 text_address='',
                 aiml_address='',
                 config_address=''):

        print(text_address, aiml_address, config_address)

        context = context or zmq.Context()
        self.text_socket = context.socket(zmq.SUB)
        self.text_socket.connect(text_address)
        self.text_socket.setsockopt(zmq.SUBSCRIBE, b'')

        self.config_socket = context.socket(zmq.REP)
        self.config_socket.bind(config_address)

        self.aiml_socket = context.socket(zmq.PUB)
        self.aiml_socket.connect(aiml_address)

        self.poller = zmq.Poller()
        self.poller.register(self.text_socket, zmq.POLLIN)
        self.poller.register(self.config_socket, zmq.POLLIN)

        aiml_path = path.dirname(aiml.__file__)
        # TODO: add in the rest of the aiml files somewhere
        self._aiml_files = path.join(aiml_path, 'standard')
        os.chdir(self._aiml_files)

        self.aiml_kernel = aiml.Kernel()
        self.aiml_kernel.learn('startup.xml')
        self.aiml_kernel.respond('load aiml b')

    def run(self):
        print('made it to run')
        while True:
            sockets = dict(self.poller.poll())
            print(sockets)

            if self.config_socket in sockets:
                self._config_socket_handler()
            elif self.text_socket in sockets:
                self._text_socket_handler()

    def _config_socket_handler(self):
        frame = self.config_socket.recv()

    def _text_socket_handler(self):
        print('made it here')
        msg = self.text_socket.recv()
        print(msg)
        response = self.aiml_kernel.respond(msg.decode('ascii'))
        self.aiml_socket.send(response.encode('ascii'))
