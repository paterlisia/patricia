import time
import threading
from sendinfo import SendInfo
import socket


class KeepLive(object):
    def __init__(self):
        pass

    def keeplive(self):
        info = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'  # heartbeat info
        SendInfo(info)  # send info every 10 seconds
        threading.Timer(40, self.keeplive).start()  # send info every 15 seconds
