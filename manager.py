import socket
import Queue
import threading
import pickle
import time
import sys
from paxos import Message, Logger


class Retriever(threading.Thread):
    def __init__(self):
        self.queue = Queue.Queue()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((socket.gethostname(), 6666))
        threading.Thread.__init__(self)

    def run(self):
        self.socket.listen(5)
        while True:
            conn, address = self.socket.accept()
            print 'Get connected from %s' % address[0]

            while True:
                cmd = conn.recv(1024)
                if len(cmd.split('#')) > 1:
                    self.queue.put(cmd)
                    break

            conn.close()


if __name__ == '__main__':

    group = sys.argv[1]

    log = open('manager.txt', 'w')

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
    #tpcSender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #tpcSender.connect(('ec2-54-244-154-181.us-west-2.compute.amazonaws.com', 7766))

    opList = []

    while True:

        if not rt.queue.empty():
            cmd = rt.queue.get(True, 3)

            print cmd

            t = cmd.split('#')
            if len(t) == 5:
                sender, status, op, txnID, opID = t
            else:
                pass

            table, column, key, value = None, None, None, None

            if op[:5] == 'write':
                __, table, column, key, value = op.split(',')
            elif op[:4] == 'read':
                __, table, column, key = op.split(',')

            sender = sender[2:]

            print sender, status, op, '#', txnID

            m = Message(Message.MSG_EXT_PROPOSE)
            if group == 'x':
                m.to = 'ec2-23-21-13-52.compute-1.amazonaws.com'
            elif group == 'y':
                m.to = 'ec2-50-16-32-171.compute-1.amazonaws.com'

            m.value = {'sender': sender, 'status': status, 'op': op, 'txnID': txnID, 'opID': opID}
            bytes = pickle.dumps(m)
            client.sendto(bytes, (m.to, 8888))

            #tpcSender.connect((d[sender], 7766))

            while True:
                ack, __ = paxos_client.recvfrom(2048)
                m = pickle.loads(ack)
                if m.command == Message.MSG_CLIENT_ACK:
                    print 'Op #%s get accepted!' % opID
                    log.write('[%s] %s @ %s\n' % (time.time(), op, txnID))
                    #tpcSender.sendall('%s#%s' % ('paxos_ready', '#'.join(t[2:])))
                    break

    log.close()