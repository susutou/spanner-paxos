import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 6666))
cmd = [
    'NVX#paxos_prepare#begin#0#0',
    'NVX#paxos_commit#begin#0#0',
    'NVX#paxos_prepare#write,x,10#0#1',
    'NVX#paxos_prepare#write,x,20#0#2',
    'NVX#paxos_prepare#read,x#0#3',
    'NVX#paxos_prepare#commit#0#4'
]


for i in range(10):
    s.send(cmd[i % len(cmd)])
    time.sleep(1)