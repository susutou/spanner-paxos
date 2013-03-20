import socket
import pickle
import time
from paxos import Message

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

to = 'ec2-23-21-13-52.compute-1.amazonaws.com'

for i in xrange(20):
    m = Message(Message.MSG_EXT_PROPOSE)
    m.value = i * 4
    #m.value = operations[i]
    m.to = 'ec2-23-21-13-52.compute-1.amazonaws.com'
    bytes = pickle.dumps(m)
    #s.sendto('[%d] Hello server!' % i, (to, 8888))
    #time.sleep(2)
    s.sendto(bytes, (m.to, 8888))