import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket
host = socket.gethostbyname('openbarrage.douyutv.com')  # get the host(8601) of Douyu
port = 8601
s.connect((host, port))         # connect the socket to Douyu


class SendInfo(object):
    def __init__(self, info):
        try:
            info = info.encode('utf-8')  # transfer it into utf-8 as requested
            data_length = len(info) + 8
            value = 689  # the type of information for client sending to the server
            infohead = int.to_bytes(data_length, 4, 'little') + int.to_bytes(data_length, 4, 'little') \
                       + int.to_bytes(value, 4, 'little')
            # transfer int into bytes and form a protocol head
            s.send(infohead+info)
            r = s.recv(1024)
            if r:
                print(r)
            else:
                pass

        except socket.error:
            time.sleep(3)

