import ftx
import pandas as pd
import ta
from math import *
import time
#from plyer import notification



APIKey = ""
APIsecret = ""
accountName = ''

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

    def getBalance(self,client, coin):
        jsonBalance = client.get_balances()

        if jsonBalance == []:
            return 0
        pandaBalance = pd.DataFrame(jsonBalance)
        #print(pandaBalance)
        if pandaBalance.loc[pandaBalance['coin'] == coin].empty:
            return 0
        else:
            return float(pandaBalance.loc[pandaBalance['coin'] == coin]['total'])

    def trunc(self, n, decimal):
        r= floor(float(n)*10**decimal)/10**decimal
        return str(r)


    def getQuantityCoin(self):
        return account.getBalance(self.client, pairSymbol)

    def getQuantityUsdt(self):
        return account.getBalance(self.client, "USD")


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
        # notification.notify(
        #     title = f"Achat du{pairSymbol} ",
        #     message = f"ordre du marché à: {account.getActualPrice()}",
        #     timeout =10
        # )
        print(buyOrder)

    def sellCoin(self,pairSymbol):
        sellOrder = self.client.place_order(
            market=pairSymbol,
            side="sell",
            price=None,
            size=trunc(self.getQuantityCoin(), myTruncate),
            type="market")
        # notification.notify(
        #     title=f"Vente du {pairSymbol}",
        #     message=f"ordre du marché à: {account.getActualPrice()}",
        #     timeout=10
        # )
        print(sellOrder)


if __name__ == '__main__':
    fiatSymbol = 'USD'
    pairSymbol = "BTC/USD"
    cryptoSymbol = 'BTC'
    myTruncate = 4

    account = account()
    while(True):
        account.dataFrame(pairSymbol)
        #print(account.getDFrame())

        #----------------------------------------------------------------------------------------------------------
        if(float(account.getQuantityUsdt())> 5 and account.df["SMA200"].iloc[-2] > account.df["SMA600"].iloc[-2]):
            #account.buyCoin(pairSymbol)
            print("opportunité d'achat")
            print("quantité d'USDT: ", account.getQuantityUsdt())
            print("quantité de", pairSymbol, ": ", account.getQuantityCoin())
            print("prix actuelle de", pairSymbol, ":", account.getActualPrice())

        elif (float(account.getQuantityCoin())> 0.0001 and account.df["SMA200"].iloc[-2] < account.df["SMA600"].iloc[-2]):
            print("opportunité de vente")
            # account.sellCoin(pairSymbol)
            print("quantité d'USDT: ", account.getQuantityUsdt())
            print("quantité de", pairSymbol, ": ", account.getQuantityCoin())
            print("prix actuelle de", pairSymbol, ":", account.getActualPrice())
        else:
             print("No opportunity")
        time.sleep(3600)



