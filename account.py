import ftx
import pandas as pd
import ta
import time
import json
from math import *
import time
from plyer import notification

cryptoSymbol = "BTC"

myTruncate = 4
#OldAPIKey = "mfeAhaAIkHsVPAq4IxRv_4kpE9DmjsKgT5q3ZsNH"
#OldAPIsecret = "NadeOit5b5xYosXaOqyA2wy3QUN5R0T1ZX501J9Y"

APIKey = "ARFjXUv2SmqZgOQAGgh8_u7ScfcIgPNKeTp_rnn-"
APIsecret = "Y5Tjtrot-hBhWUG6swyXSdkL5YX4fL-_LsMJYkwd"
accountName = "test"
class account:
    def __init__(self):
        self.client = ftx.FtxClient(api_key=APIKey, api_secret=APIsecret, subaccount_name=accountName)
        self.df = None
    def dataFrame(self, pairSymbol):
        data = self.client.get_historical_data(
            market_name= pairSymbol,
            resolution= 3600,
            limit= 650,
            start_time= float(round(time.time()))-650*3600,
            end_time= float(round(time.time())))
        self.df = pd.DataFrame(data)
        self.df["SMA200"]= ta.trend.sma_indicator(self.df["close"], 200)
        self.df["SMA600"] = ta.trend.sma_indicator(self.df["close"], 600)

    def getDFrame(self):
        return self.df

    def getBalance(self, coin):
        jsonBalance = self.client.get_balances()
        pandaBalance = pd.DataFrame(jsonBalance)
        if pandaBalance.empty:
            print("pas de crypto, pas de usdt")
        #if pandaBalance.loc[pandaBalance["coin"] == coin].empty:
            #return 0
        #else:
            #return float(pandaBalance.loc[pandaBalance["coin"] == coin]["free"])

    def trunc(self, n, decimal):
        r= floor(float(n)*10**decimal)/10**decimal
        return str(r)


    def getQuantityCoin(self, cryptoSymbol):
        return account.getBalance(cryptoSymbol)

    def getQuantityUsdt(self):
        return account.getBalance("USD")


    def getActualPrice(self):
        self.dataFrame(pairSymbol)
        return self.df["close"].iloc[-1]

    def buyCoin(self, pairSymbol):
        quantityBuy = trunc(float(self.getQuantityUsdt())/self.getActualPrice(), myTruncate)
        buyOrder = self.client.place_order(
            market=pairSymbol,
            side="buy",
            price= None,
            size= quantityBuy,
            type="market")
        notification.notify(
            title = "Achat du BTC/USDT",
            message = f"ordre du marché à: {account.getActualPrice()}",
            timeout =10
        )
        #print(buyOrder)

    def sellCoin(self,pairSymbol):
        sellOrder = self.client.place_order(
            market=pairSymbol,
            side="sell",
            price=None,
            size=trunc(self.getQuantityCoin(), myTruncate),
            type="market")
        notification.notify(
            title="Vente du BTC/USDT",
            message=f"ordre du marché à: {account.getActualPrice()}",
            timeout=10
        )
        #print(sellOrder)


if __name__ == '__main__':
    pairSymbol = "BTC/USD"
    account = account()
    while(True):
        account.dataFrame(pairSymbol)
        print(account.getDFrame())
        print(account.getQuantityUsdt())
        print(account.getQuantityCoin(cryptoSymbol))
        print(account.getActualPrice())

        #----------------------------------------------------------------------------------------------------------
        if(float(account.getQuantityUsdt())> 5 and account.df["SMA200"].iloc[-2] > account.df["SMA600"].iloc[-2]):
            account.buyCoin(pairSymbol)

        elif (float(account.getQuantityCoin())> 0.0001 and account.df["SMA200"].iloc[-2] < account.df["SMA600"].iloc[-2]):
            account.sellCoin(pairSymbol)
        time.sleep(60)



