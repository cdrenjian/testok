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
            else:
                print('%s价格未变 趋势值%s'%(self.name,self.trend))
        start_all(self.api)



    def jude_trend(self):
        if self.new_price>self.old_price:
            print('上升')
            self.trend += 1
        else:
            print('下降')
            self.trend -= 1
        self.old_price=self.new_price
        if self.on_hand is None: #未正确获取到持有值，直接返回不往下执行
            return  None
        if not self.on_hand and self.trend>4:
            self.in_trade()
            self.trend=1
        elif self.on_hand and self.trend<-4:
            self.out_trade()
            self.trend=-1
        elif self.trend>5 :
            self.trend=1
        elif self.trend<-5:
            self.trend=-1
        return None
    def in_trade(self):
        print('准备买入')
        while not self.on_hand:
            self.money=self.api.get_user_info('usdt')
            if float(self.money)<5:
                return None
            count=float(self.money)/(float(self.new_price)*2)
            id=self.api.buy(self.name,float(self.buy1)+0.01,count)
            time.sleep(15)
            self.on_hand = self.api.get_user_info(self.name)
            self.api.cancel(self.name,id)
            time.sleep(2)



    def out_trade(self):
        print('准备卖出')
        while  self.on_hand:
            count=self.on_hand
            id=self.api.sell(self.name,float(self.sell1-0.01),count)
            time.sleep(15)
            self.on_hand = self.api.get_user_info(self.name)
            self.api.cancel(self.name,id)
            time.sleep(2)


def start_all(api):
    global lock
    if lock:
        return None
    lock=True
    aims=api.update_pairs()
    on_hands=api.get_on_hands()
    for h in on_hands:
        aims.append(h)
    print('aims:%s'%aims)
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

