import socket
import threading
import re
from keeplive import KeepLive
from one_category import GetRoomInfo

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # create a socket
host = socket.gethostbyname('openbarrage.douyutv.com')  # get the host(8601) of Douyu
port = 8601
s.connect((host, port))         # connect the socket to Douyu
Bullet_comment = re.compile(b'txt@=(.+?)/cid@')


def sendinfo(info):
    info = info.encode('utf-8')  # transfer it into utf-8 as requested
    data_length = len(info) + 8
    value = 689  # the type of information for client sending to the server
    infohead = int.to_bytes(data_length, 4, 'little') + int.to_bytes(data_length, 4, 'little') \
               + int.to_bytes(value, 4, 'little')
    # transfer int into bytes and form a protocol head
    s.send(infohead + info)


# log in
def get_txt(roomid):
    info = 'type@=loginreq/roomid@={}\0'.format(str(roomid))  # sending login request
    sendinfo(info)
    info_joingroup = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(str(roomid))  # sending joingruop request
    sendinfo(info_joingroup)
    while True:
        data = s.recv(1024)
        data_now = Bullet_comment.findall(data)
        if data:
            for i in range(0, len(data_now)):
                with open(str(roomid), 'a') as f:  # create a txt.file to save data
                    try:
                        # print(data_now[0].decode(encoding='utf-8'))
                        txt = data_now[0].decode(encoding='utf-8') + '\n'  # save data
                        f.writelines(txt)
                    except AttributeError:
                        print('Error')
        else:
            break


# send heartbeat information
def keeplive():
    keep_live = KeepLive()  # create an instance
    keep_live.keeplive()


def main():
    all_room = GetRoomInfo(1, [])
    all_room.get_all_rooms()
    room_info = all_room.room_info
    room_id = []
    print(len(room_info))
    for i in range(len(room_info)):
        id = room_info[i].get('room_id')
        room_id.append(id)  # get room_id
        pro1 = threading.Thread(target=get_txt(room_id[i]))  # process1 for get bullet comments of every room
        pro1.start()
        pro2 = threading.Thread(target=keeplive())  # process2 for keeplive
        pro2.start()


if __name__ == '__main__':
    main()
