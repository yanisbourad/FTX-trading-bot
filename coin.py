from binance.client import Client
import pandas as pd
import ta
import matplotlib.pyplot as plt
import time
from plyer import notification

class coin:
    def __init__(self, symb, date, intervalle):
        self.symb = symb
        self.date = date
        self.intervalle = intervalle
        self.klinest = 0
        self.df = 0
    def setInfoCoin(self):
        self.klinest = Client().get_historical_klines(self.symb, self.intervalle, self.date)

    def getInfoCoin(self):
        self.setInfoCoin()
        return self.klinest

    def initializeDataframeCoin(self):
        self.setInfoCoin()
        self.df = pd.DataFrame(self.getInfoCoin(), columns=["timestamp", "open", "high", "low", "close",
                                            "volume", "close_time", "quote_av", "trades", "tb_base_av", "tb_quote_av",
                                            "ignore"])

        del self.df["close_time"]
        del self.df["quote_av"]
        del self.df["trades"]
        del self.df["tb_base_av"]
        del self.df["tb_quote_av"]
        del self.df["ignore"]

        self.df["open"] = pd.to_numeric(self.df["open"])
        self.df["high"] = pd.to_numeric(self.df["high"])
        self.df["low"] = pd.to_numeric(self.df["low"])
        self.df["close"] = pd.to_numeric(self.df["close"])
        self.df["volume"] = pd.to_numeric(self.df["volume"])

        self.df = self.df.set_index(self.df["timestamp"])
        self.df.index = pd.to_datetime(self.df.index, unit="ms")
        del self.df["timestamp"]
        self.df["SMA200"] = ta.trend.sma_indicator(self.df["close"], 200)
        self.df["SMA600"] = ta.trend.sma_indicator(self.df["close"], 600)

    def getDataframeCoin(self):
        #print(self.initializeDataframeCoin())
        return self.df

    def getAllInfoCoin(self):
        return self.getDataframeCoin.iloc[-1]

    def getLastOpenPrice(self):
        return self.getDataframeCoin().iloc[-1]["open"]

    def getLastHighPrice(self):
        return self.getDataframeCoin.iloc[-1]["high"]

    def getLastLowPrice(self):
        return self.getDataframeCoin.iloc[-1]["low"]

    def getLastClosePrice(self):
        return self.getDataframeCoin.iloc[-1]["close"]

    def getLastVolume(self):
        return self.getDataframeCoin.iloc[-1]["volume"]

    def getName(self):
        return self.symb



    def plotGraph(self):
        #self.setIndicator(line1, line2, num1, num2)
        self.df["SMA200"] = ta.trend.sma_indicator(self.df["close"], 200)
        data= self.getDataframeCoin()
        plt.cla()
        plt.plot(data.index, self.df["volume"])
        plt.xlabel("time")
        plt.ylabel("price")
        plt.title(self.symb)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    btc = coin("BTCUSDT","08 february 2022","1m")
    btc.initializeDataframeCoin()
    btc.getDataframeCoin()
    #print(f"la dernière données du {btc.getName()}: ")
    print(btc.getDataframeCoin())
    btc.plotGraph()
    #print(float(eth.getInfoCoin()[-1][4]))
    notification.notify(
        title="Vente du BTC/USDT",
        message=f"ordre du marché à: {float(btc.getInfoCoin()[-1][4])}",
        timeout=10
    )

