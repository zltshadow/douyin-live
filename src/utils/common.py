import requests
import json
from utils.config import LIVE_WEB_SEND_URL, GAME_UUID, DONATION_UUID


class GlobalVal(object):
    # 点赞总数
    like_num = 0
    # 评论总数
    commit_num = 0
    # 礼物数量和价值
    gift_num = 0
    gift_value = 0
    # 特殊礼物：月下瀑布
    gift_list = []
    # 礼物id列表：礼物去重使用，因为有送一个礼物，但是抖音监听到两个礼物的情况
    gift_id_list = []
    # 记录直播间人数
    member_num = 0
    # 在线观众排名
    rank_user = []


# 初始化全局变量：从服务端获取
def init_global():
    payload = json.dumps({
        "taskuuid": "querydonation",
        "gameuuid": GAME_UUID
    })
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", LIVE_WEB_SEND_URL, headers=headers, data=payload)
        query_json = response.json()
        game_data = query_json.get("response_data").get("data")
        for data in game_data:
            if data.get("uuid") == DONATION_UUID:
                GlobalVal.like_num = data.get("applypoint")
                GlobalVal.commit_num = data.get("popmsg")
                GlobalVal.gift_value = data.get("giftlist")
                GlobalVal.gift_list = [i for i in data.get("fannamereadylist").split("|") if i]
                return
    except Exception as e:
        print(f"获取线上数据失败：如果你不用将直播数据推送到你们的服务器上，可以忽略此提示")
