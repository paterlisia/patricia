import requests
import json


class GetRoomInfo(object):
    def __init__(self, cate_id, room_info):
        self.room_info = room_info
        self.cate_id = cate_id

    def get_all_rooms(self):
            url = "http://open.douyucdn.cn/api/RoomApi/live/" + str(self.cate_id)
            room_info = requests.get(url)
            room_info = room_info.text
            room_info = json.loads(room_info)["data"]
            self.room_info = room_info

