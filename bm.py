import bitmex
import json
from market import Ticker
import threading
key="B-ShzKBPVbBoptaeL2UsR0BI"
secert="PqUDgdHt2zTxQKXu_QKq-bgQWZfurgmzkPXKat-ZrQd68T7D"
# client = bitmex.bitmex(test=False, api_key=key, api_secret=secert)
# r=client.OrderBook.Order_book_get_l2(symbol='XBTUSD').result()
import time
part=300.0
max_order = 5
postion_check=6
reduce_count=3
f_oldsize = 0
h_oldsize = 0
m_enough=True
old_p=0
old_b=0
symbol1='XBTUSD'
symbol2='XBTH18'
# def get_operations(Api):
#     r = Api.operations.items()
#     print(r)
#
# get_operations(client.User)
# r=client.OrderBook.OrderBook_getL2(symbol='XBTUSD').result()
# r=client.Trade.Trade_get(symbol='XBTUSD').result()
# f=client.Position.Position_get(filter="""{"symbol":"XBTUSD"}""").result()[0][0]
# print(r['lastPrice'])
# print(r['currentQty'])
# print(r['liquidationPrice'])
#['APIKey', 'Announcement', 'Chat', 'Execution', 'Funding', 'Instrument', 'Insurance', 'Leaderboard', 'Liquidation', 'Notification', 'Order', 'OrderBook', 'Position', 'Quote', 'Schema', 'Settlement', 'Stats', 'Trade', 'User']




class Bx(object):
    def __init__(self):
        self.client = bitmex.bitmex(test=False, api_key=key, api_secret=secert)
        self.position_change()

    # def change(self,direct,symbol,position):
    #     """用于实际调整positions,执行操作"""
    #     global old_p
    #     print('change beigin')
    #     p, q, f = self.get_stats_by_rest({"symbol": symbol})
    #     if int(p)!=old_p:
    #         old_p=int(p)
    #     else:
    #         print('price not change')
    #         return False
    #     if direct==0:
    #         print('not action')
    #         return False
    #     elif direct==-1:
    #         if position < 0:
    #             side ='Buy'
    #             p=p*0.9998
    #         else:
    #             side='Sell'
    #             p=p*1.0002
    #         self.order(symbol,side=side,p=p)
    #     else:
    #         if position < 0:
    #             side = 'Sell'
    #             p=p*1.0002
    #         else:
    #             side = 'Buy'
    #             p=p*0.9998
    #         self.order(symbol,side=side,p=p)
    #     return True
    def get_available_m(self):
        r=self.client.User.User_getMargin().result()[0]
        m=r['availableMargin']/100000.0
        print('available:%s'%m)
        return m


    def keep_away(self):
        pass
    # def direction(self):
    #     """判断操作方向"""
    #     direct=0
    #     print('direction beigin')
    #     global f_oldsize
    #     global h_oldsize
    #     fp, fq, ff = self.get_stats_by_rest({"symbol": "XBTUSD"})
    #     hp, hq, hf = self.get_stats_by_rest({"symbol": "XBTH18"})
    #     if not fp or not fq or not ff or not hp or not hq or not hf:
    #         direct=0
    #         return direct
    #     self.fq=fq
    #     self.hq=hq
    #     self.ff=ff
    #     self.hf=hf
    #     self.fp=fp
    #     self.hp=hp
    #     more=fq + hq
    #     if more*fq>0:
    #         symbol="XBTUSD"
    #         f_newsize=abs(self.ff-self.fp)
    #         if f_newsize==f_oldsize:
    #             direct=0
    #         elif f_newsize>f_oldsize+58:
    #             direct=-1
    #         elif f_newsize<208:
    #             direct=1
    #         f_oldsize=f_newsize
    #         position=self.fq
    #     else:
    #         symbol="XBTH18"
    #         h_newsize=abs(self.hf-self.hp)
    #         if h_newsize==h_oldsize:
    #             direct=0
    #         elif h_newsize>h_oldsize+58:
    #             direct=-1
    #         elif h_newsize<208:
    #             direct=1
    #         h_oldsize=h_newsize
    #         position=self.hq
    #     return direct,symbol,position

    def start(self):
        """建立position"""
        global postion_check,reduce_count
        while True:
            # direct,symbol,position=self.direction()
            # self.change(direct,symbol,position)
            d=self.get_distance()
            f = self.get_stats('XBTUSD')
            h = self.get_stats('XBTH18')
            fa=f['ask']
            fb=f['bid']
            ha=h['ask']
            hb=h['bid']
            if not fa or not fb or not ha or not hb:
                continue
            reduce_count=1 #每次流程前均认为不减
            if d==1:
                print("入")
                self.order('XBTUSD', 'Buy', fb)
                self.order('XBTH18', 'Sell', ha)
            elif d==-1:
                print('出')
                self.order('XBTUSD', 'Sell', fa)
                self.order('XBTH18', 'Buy', hb)
                # self.order('XBTUSD', 'Buy', fb)
                # self.order('XBTH18', 'Sell', ha)
            else:
                print('not action')
            if postion_check>0:
                postion_check=postion_check-1
            else:
                postion_check=6
                symbol,side=self.position_change()  #调整位置平衡
                s= self.get_stats(symbol)
                sa = s['ask']
                sb = s['bid']
                if side==-1:
                    self.order(symbol, 'Sell', sa)
                elif side==1:
                    self.order(symbol, 'Buy', sb)
            time.sleep(2)









    def get_distance(self):
        global reduce_count,part,m_enough,postion_check
        if postion_check==0:
            reduce_count=reduce_count-1
        # if reduce_count<0:
        #     part=2*part
        #     reduce_count=0
        #     if self.fq>0:
        #         return -1
        #     else:
        #         return  1
        f=self.get_stats('XBTUSD')
        h=self.get_stats('XBTH18')
        hm=h['markPrice']
        fm=f['markPrice']
        distance=hm-fm
        self.is_force_close(hm,fm)
        if distance>=80:
            return 1
        elif distance<30:
            return -1
        else:
            m_enough=False
            postion_check=-1
            return 0

    def is_force_close(self,hm,fm):
        global part
        if abs(self.ff-fm)<80:
            f = self.get_stats(symbol1)
            fa = f['ask']
            fb = f['bid']
            part = self.fq
            if self.fq<0:
                self.order(symbol1,'Buy',fb)
            else:
                self.order(symbol1, 'Sell', fa)
        if abs(self.hf-hm)<80:
            h = self.get_stats(symbol2)
            ha = h['ask']
            hb = h['bid']
            part = self.hq
            if self.hq<0:
                self.order(symbol2,'Buy',hb)
            else:
                self.order(symbol2, 'Sell', ha)


    def get_positions(self):
        return self.fq,self.hq

    def get_stats_by_rest(self,symbol={"symbol": "XBTUSD"}):
        print('begin rebanlance position')
        try:
            r = self.client.Position.Position_get(filter=json.dumps(symbol)).result()[0][0]
        except Exception as e:
            print(e)
            return 0, 0, 0
        try:
            p = r['lastPrice']
            q = r['currentQty']
            f = r['liquidationPrice']
        except Exception as e:
            print(e)
            return 0, 0, 0
        print(r['lastPrice'])
        print(r['currentQty'])
        print(r['liquidationPrice'])
        return p, q, f

    def get_stats(self,symbol):
        """得到最新状态"""
        result=t.get_stats()
        for i in result:
            if i['symbol']==symbol:
                stats=i
                return stats
        return None

    def change_leverage(self):
        """用于增加lever"""
        #Position_updateLeverage
        pass
        return True

    def order(self,symbol,side,p):
        global  max_order,old_b,postion_check,reduce_count,part,m_enough
        print('order beigin')
        # time.sleep(2)
        # p=float(int(p))
        # if p==old_b:
        #     print('not price change')
        #     return False
        # else:
        #     old_b=p
        if not m_enough and  reduce_count>0:
            print('not m to buy')
            return False
        try:
            r=self.client.Order.Order_new(symbol=symbol,side=side,orderQty=part,price=p,execInst="ParticipateDoNotInitiate").result()[0]
            print(r)
            part=300
            if not m_enough:
                time.sleep(15)
        except Exception as  e:
            print('异常%s'%e)
            if 'Account has insufficient Available Balance' in str(e):
                reduce_count=-1
                m_enough=False
                print('not enough m')

                return False
        print('order sueccs')
        part=300
        max_order=max_order-1
        if max_order<0:
            self.cancel_all()
            try:
                self.client.Position.Position_updateLeverage(symbol=symbol,leverage=25.0)
            except Exception as e:
                print(e)
            max_order=5


        # order_new(symbol, side=side, simple_order_qty=simple_order_qty, quantity=quantity, order_qty=order_qty,
        #           price=price,
    def cancel_all(self):
        global m_enough
        time.sleep(3)
        print('chancel')
        if not m_enough:
            if self.get_available_m()>3.8:
                m_enough=True
        try:
            print(self.client.Order.Order_cancelAll().result())
        except Exception as e:
            print(e)
        return True

    def position_change(self):
        global part,m_enough,reduce_count
        fp, fq, ff = self.get_stats_by_rest({"symbol": symbol1})
        hp, hq, hf = self.get_stats_by_rest({"symbol": symbol2})
        afq=abs(fq)
        ahq=abs(hq)
        self.fq=fq
        self.hq=hq
        self.ff=ff
        self.hf=hf
        if afq>ahq:
            part=afq-ahq
            if fq<0:
                if not m_enough:
                    part=400
                    reduce_count=-1
                    return symbol1, 1
                return symbol2, 1
            elif not m_enough:
                part=400
                reduce_count=-1
                return symbol1, -1
            return symbol2, -1
        elif afq<ahq:
            part=ahq-afq
            if hq<0:
                if not m_enough:
                    part=400
                    reduce_count=-1
                    return symbol2, 1
                return symbol1, 1
            elif not m_enough:
                part=400
                reduce_count=-1
                return symbol2, -1
            return symbol1, -1
        else:
            return symbol1,0




if __name__=='__main__':
    print('start')
    t=Ticker()
    k=Bx()
    th=threading.Thread(target=t.run)  #持续更新状态值
    th.start()
    k.start()

