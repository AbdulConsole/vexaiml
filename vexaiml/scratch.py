from __future__ import print_function
import atexit

from threading import Thread
from time import sleep
import zmq

from aiml_parser import AIMLParser


context = zmq.Context()
text_sender = context.socket(zmq.PUB)
text_address = 'tcp://127.0.0.1:5571'
text_sender.bind(text_address)

response_socket = context.socket(zmq.SUB)
response_socket.setsockopt(zmq.SUBSCRIBE, b'')
response_address = 'tcp://127.0.0.1:5556'
response_socket.bind(response_address)

# doesn't matter what this is, not going to use
config_address = 'tcp://127.0.0.1:5557'
sleep(1)

aiml = AIMLParser(None, text_address, response_address, config_address)

thread_instance = Thread(target=aiml.run)
thread_instance.start()
def _kill_thread():
    thread_instance.join(.2)

atexit.register(_kill_thread)

msg = b'Hey, good morning'
text_sender.send(msg)
try:
    print('waiting for rsp')
    rsp = response_socket.recv()
    print(rsp)
except KeyboardInterrupt:
    pass
thread_instance.join(0.2)
