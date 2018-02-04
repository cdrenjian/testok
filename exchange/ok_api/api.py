from ok_api.OkcoinSpotAPI import OKCoinSpot
import json
from tools.send_mail import Mail
from tools.get_last_up import Uppairs
import time


apikey = '4eee8a24-d55b-4211-b16f-201e7f22309d'
secretkey = "9A1407F07E222D380CA20C0414808444"
okcoinRESTURL = 'www.okex.com'

mail = Mail()

class  Ok_Api(object):
    def __init__(self):
        self.spot = OKCoinSpot(okcoinRESTURL, apikey, secretkey)
        self.paris=Uppairs('okex')
        self.on_hands=set()
    def update_pairs(self):
        return  self.paris.update()


    def get_on_hands(self):
        try:
            time.sleep(1)
            r = json.loads(self.spot.userinfo())
            for k, v in r['info']['funds']['free'].items():
                if float(v) > 1 and k!='usdt':
                    self.on_hands.add(k + '_usdt')
        except Exception as e:
            print(e)
        return self.on_hands
    def get_user_info(self,name='btc'):
        c=name.split('_')[0]
        try:
            time.sleep(1)
            r=json.loads(self.spot.userinfo())
            hand=r['info']['funds']['free'][c]
        except Exception as e:
            print(e)
            return None
        if float(hand)<0.5:
            hand=0
        return  hand

    def buy(self,name='ltc_usd',price=1,count=1):
        print('下买单%s'%name)
        mail.send_mail('入场%s'%name)
        try:
            time.sleep(1)
            r=json.loads(self.spot.trade(name,'buy',price,count))
        except Exception as e:
            print(e)
            r={}
        print(r.get('order_id'))
        return r.get('order_id')

    def sell(self,name='ltc_usd',price=1,count=1):
        print('下卖单%s'%name)
        mail.send_mail('出场%s'%name)
        try:
            time.sleep(1)
            r = json.loads(self.spot.trade(name,'sell',price,count))
        except Exception as e:
            print(e)
            r={}
        print(r.get('order_id'))
        return r.get('order_id')


    def situation(self,name='ltc_btc'):
        try:
            time.sleep(1)
            r = self.spot.ticker(name)
        except Exception as e:
            print(e)
            return 999.99,999.99,999.99
        print(r['ticker']['last'])
        return float(r['ticker']['last']),float(r['ticker']['buy']),float(r['ticker']['sell'])
    def cancel(self,name='ltc_usd',id=-1):
        try:
            time.sleep(1)
            self.spot.cancelOrder(name, id)
        except Exception as e:
            print(e)
        return True
