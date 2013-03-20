import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# cmd = [
#     'ORX#paxos_prepare#begin#0#0',
#     'ORX#paxos_commit#begin#0#0',
#     'ORX#paxos_prepare#write,x,10#0#1',
#     'ORX#paxos_prepare#write,x,20#0#2',
#     'ORX#paxos_prepare#read,x#0#3',
#     'ORX#paxos_prepare#commit#0#4'
# ]





s.connect(('ec2-23-21-13-52.compute-1.amazonaws.com', 6666))
s.send('ORX#paxos_prepare#commit#0#0')
s.close()