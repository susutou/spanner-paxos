# import xmlrpclib
#
# server = xmlrpclib.ServerProxy('http://ec2-54-244-154-181.us-west-2.compute.amazonaws.com:7777')
#
# server.algdemo.addRecord('CS271', 'mykey2', 'credit', '', 'a-test-insert2')
# server.algdemo.addRecord('CS271', 'mykey3', 'credit', '', 'a-test-insert3')
# server.algdemo.addRecord('CS271', 'mykey4', 'credit', '', 'a-test-insert4')
# server.algdemo.addRecord('CS271', 'mykey5', 'credit', '', 'a-test-insert5')

f = file('log.txt', 'a+')
f.write('test')
f.close()