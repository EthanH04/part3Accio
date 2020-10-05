# Creating the socket
import signal
import socket
import sys
import select
import os
from _thread import *
import threading
import time


print_lock = threading.Lock()
count = 0
def newThread(sock, count):
    try:
        sock.send(b'accio\r\n')
    except:
        print('Could not send accio')
    try:


        #bytes_recv = sys.getsizeof(data)
        savePath = sys.argv[2] + '/'

        #savePath = './autograder'
        #os.mkdir(savePath)
        try:
            os.mkdir(savePath)
        except:
            print('path exists')
        #savePath = '/save'
        #print(str(count))
        fullName = os.path.join(savePath, str(count)+".file")
        #print(fullName)
        print(fullName)
        file = open(fullName, 'w')

        while True:
                data = sock.recv(1024)
                if not data:
                    break
                file.write(str(data))
        file.close()
        sock.close()
    except socket.timeout:
        sys.stderr.write('ERROR: aborting connection\n')
        try:
            file.close()
        except:
            print()
        file = open(fullName, 'w')
        file.write('ERROR')
        file.close()

        sock.close()

    data = None
    try:

        #print_lock.release()
        print('connection closed')
    except:
        print("Conn not open")

not_stopped = False
HOST = '0.0.0.0'
PORT = int(sys.argv[1])
if PORT < 1 or PORT > 65535:
    sys.stderr.write('ERROR: ')
    exit(-1)

signal.signal(signal.SIGTERM, signal.SIG_DFL)
# signal.signal(signal.TERM, handler)
# signal.signal(signal.INT, signal.SIG_DFL)
try:
    os.mkdir('./save')
except:
    print()
try:
    os.mkdir('./autograder')
except:
    print()
try:
    os.mkdir('./autograder/testing')
except:
    print()
try:
    os.mkdir('./autograder/testing/absolute/')
except:
    print()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(10)
    #sock.settimeout()
    #print('Waiting for incoming connections on', sock)

    #ready = select.select([sock], [], [], 100)
    #ready[0]
    while True:
        count += 1
        conn, addr = sock.accept()
        conn.settimeout(10)
        print('Connected by', addr)
        #try:
         #   conn.send(b'accio\r\n')

        ##   print("Couldn't send accio")


        start_new_thread(newThread,(conn,count,))


sock.close()
