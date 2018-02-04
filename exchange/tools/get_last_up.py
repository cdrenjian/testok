import requests
import time
main_url='https://data.block.cc/api/v1'

class Uppairs(object):
    def __init__(self,exchange):
        self.ex_name=exchange
        self.get_support()


    def get_support(self):
        self.support_usdt=[]
        api_url=main_url+'/market/'+self.ex_name
        r=requests.get(api_url).json()
        while r['message']!='success':
            time.sleep(1)
            api_url = main_url + '/market/' + self.ex_name
            r = requests.get(api_url)
        for i in r['data']['symbol_pairs']:
            if i.split('_')[1] == 'USDT':
                self.support_usdt.append(i.lower())
        print(self.support_usdt)
    def update(self):
        self.up=[]
        print('开始搜索上升对....')
        for pair in self.support_usdt:
            api_url=main_url+'/kline?market={0}&symbol_pair={1}&types=5m&limit=3'.format(self.ex_name,pair)
            r = requests.get(api_url).json()
            while r['message'] != 'success':
                r = requests.get(api_url).json()
            r= r['data']
            try:
                if  r[2][2] <39 and r[2][2]>r[1][2]:
                    self.up.append(pair)
            except Exception as e:
                print(e)
                continue
        return self.up

    def get_HighExchange(self):
        self.high=[]
        print('开始搜索高量对....')
        api_url='https://block.cc/api/v1/exchange/tickers?name={0}&page=0&size=50'.format(self.ex_name)  #获取24小时交易量排行
        r = requests.get(api_url).json()
        print(r)
        while r['message'] != 'success':
            r = requests.get(api_url).json()
        r= r['data']['tickers']
        try:
            for data in r[3:40]:
                pair = data['url'].split('#')[1]
                print(pair)
                if pair[-4:] == 'usdt':
                    self.high.append(pair)
        except Exception as e:
            print(e)
        print(self.high)
        return self.high



p=Uppairs('okex')
p.get_HighExchange()