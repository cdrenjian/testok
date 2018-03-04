import time
import threading
from ok_api.api import  Ok_Api
from tools.send_mail import Mail
from tools.get_last_up import  Uppairs



class Trade(object):
    def __init__(self,name,api):
        #初始化对应api配置
        self.name = name
        self.api = api
        self.old_price,self.buy1,self.sell1 = self.api.situation(self.name)
        self.trend=0
        self.on_hands=set()
    def listen(self):
        for i in range(300):
            time.sleep(5)
            self.on_hand=self.api.get_user_info(self.name)
            if self.on_hand:
                print('%s当前已持有%s'%(self.name,self.on_hand))
            else:
                print('%s尚未持有'%self.name)
            self.new_price,self.buy1,self.sell1 = self.api.situation(self.name)
            if self.new_price!=self.old_price:
                self.jude_trend()
        start_all(self.api)



    def jude_trend(self):
        self.old_price=self.new_price
        if self.on_hand is None: #未正确获取到持有值，直接返回不往下执行
            return  None
        self.in_trade()
        self.out_trade()
        return None
    def in_trade(self):
        print('准备买入')
        self.money=self.api.get_user_info('usdt')
        if float(self.money)<5:
            return None
        count=float(self.money)/(float(self.new_price)*10)
        id1=self.api.buy(self.name,float(self.buy1*0.99),count)
        p=float(self.buy1*0.99)
        print('欲买价%s'%p)
        time.sleep(60)
        count=float(self.money)/(float(self.new_price)*10)
        time.sleep(30)
        self.api.cancel(self.name,id1)
        time.sleep(2)



    def out_trade(self):
        print('准备卖出')
        count=float(self.on_hand)/3.0
        id=self.api.sell(self.name,float(self.sell1*1.006),count)
        time.sleep(60)
        self.on_hand = self.api.get_user_info(self.name)
        self.api.cancel(self.name,id)
        time.sleep(2)


def start_all(api):
    aims=['xrp_usdt','eos_usdt','bch_usdt','iota_usdt','eth_usdt','ltc_usdt']
    for i in aims:
        t= Trade(i, api)
        th=threading.Thread(target=t.listen)
        th.start()
    time.sleep(600)
    lock=False



if __name__=='__main__':
    lock=False
    ok_ex=Ok_Api()
    mail=Mail()
    start_all(ok_ex)

