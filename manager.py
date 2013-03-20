import socket
import Queue
import threading
import pickle
import time
import sys
from paxos import Message


class Retriever(threading.Thread):
    def __init__(self):
        self.queue = Queue.Queue()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((socket.gethostname(), 6666))
        threading.Thread.__init__(self)

    def run(self):
        self.socket.listen(1)
        while True:
            conn, address = self.socket.accept()
            cmd = conn.recv(2048)
            if cmd is not None and len(cmd.split('#')) == 5:
                self.queue.put(cmd)
                #print cmd


if __name__ == '__main__':

    group = sys.argv[1]

    d = {
        'NVX': 'ec2-23-21-13-52.compute-1.amazonaws.com',
        'NVY': 'ec2-50-16-32-171.compute-1.amazonaws.com',
        'ORX': 'ec2-54-244-154-181.us-west-2.compute.amazonaws.com',
        'ORY': 'ec2-54-245-188-21.us-west-2.compute.amazonaws.com',
        'EUX': 'ec2-54-228-101-94.eu-west-1.compute.amazonaws.com',
        'EUY': 'ec2-54-228-106-12.eu-west-1.compute.amazonaws.com'
    }

    rt = Retriever()
    rt.start()

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    paxos_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    paxos_client.bind((socket.gethostname(), 6667))
    tpcSender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    opList = []

    while True:

        if not rt.queue.empty():
            cmd = rt.queue.get(True, 3)
            t = cmd.split('#')
            if len(t) == 5:
                sender, status, op, txnID, opID = t
            else:
                continue

            key, value = None, None

            if op[:5] == 'write':
                __, key, value = op.split(',')
            elif op[:4] == 'read':
                __, key = op.split(',')

            print sender, status, op, '#', txnID

            m = Message(Message.MSG_EXT_PROPOSE)
            if group == 'x':
                m.to = 'ec2-23-21-13-52.compute-1.amazonaws.com'
            elif group == 'y':
                m.to = 'ec2-50-16-32-171.compute-1.amazonaws.com'

            m.value = {'sender': sender, 'status': status, 'op': op, 'txnID': txnID, 'opID': opID}
            bytes = pickle.dumps(m)
            client.sendto(bytes, (m.to, 8888))

            while True:
                ack, __ = paxos_client.recvfrom(2048)
                try:
                    m = pickle.loads(ack)
                    if m.command == Message.MSG_CLIENT_ACK:
                        print 'Op #%s get accepted!' % opID
                        tpcSender.connect((d[sender], 7766))
                        tpcSender.send('%s#%s' % ('paxos_ready', '#'.join(t[2:])))
                        tpcSender.close()
                        break
                except:
                    pass
