# from bitmex_websocket import BitMEXWebsocket
#
#
# ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/api/v1", symbol="XBTUSD",
#  api_key='"B-ShzKBPVbBoptaeL2UsR0BI"',
#  api_secret='PqUDgdHt2zTxQKXu_QKq-bgQWZfurgmzkPXKat-ZrQd68T7D')

import json
import hashlib
import hmac
import json
import time
import urllib

from websocket import create_connection
# ws = create_connection("wss://www.bitmex.com/realtime?subscribe=quote:XBTUSD")
# #ws.connect("wss://api2.bitfinex.com:3000/ws")
# # ws.send(json.dumps({
# #     "event": "subscribe",
# #     "channel": "book",
# #     "pair": "BTCUSD",
# #     "prec": "P0"
# # }))
#
#
# while True:
#     result = ws.recv()
#     result = json.loads(result)
#     print(type(result))
#     if result.get('data'):
#         data=result['data']
#         if data[0].get('bidPrice'):
#             r = data[0]['bidPrice']
#             print('bid%s'%r)
#             r = data[0]['askPrice']
#             print('ask:%s'%r)
#     print ("Received '%s'" % result)
#
# ws.close()

stats=[
       {'symbol':'XBTUSD','markPrice':0,'bid':0,'ask':0},
       {'symbol':'XBTH18','markPrice':0,'bid':0,'ask':0}
       ]

class Ticker(object):
    def __init__(self):
        self.ws = create_connection("wss://www.bitmex.com/realtime?subscribe=instrument:XBTUSD,instrument:XBTH18,quote:XBTH18,quote:XBTUSD")

    def update(self,symbol,key,value):
        global stats
        for i in  stats:
            if i['symbol']==symbol:
                i[key]=value

    def run(self):
        while True:
            self.update_stats()

    def update_stats(self):
        global stats
        result = self.ws.recv()
        result = json.loads(result)
        if result.get('data'):    #得到一条更新数据
            data = result['data']
            if data[0].get('symbol'):
                symbol = data[0]['symbol']
            else:
                return None   #无标志数据视为无效
            if data[0].get('bidPrice') and data[0].get('askPrice'):
                r = data[0]['bidPrice']
                self.update(symbol,"bid",r)
                r = data[0]['askPrice']
                self.update(symbol,"ask",r)
            if data[0].get('markPrice'):
                mp=data[0]['markPrice']
                self.update(symbol,'markPrice',mp)
    def get_stats(self):
        return stats



