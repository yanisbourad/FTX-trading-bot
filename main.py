# On import api de binance pour importer les cours du marche
#on import pandas pour gerer les tableaux facilement
#

from binance.client import Client
import pandas as pd
import ta
import matplotlib.pyplot as plt

# on import les resultat du cours du marché du BTCUSDT, a partir du 1 janvier 2021, a chaque une heure
klinest = Client().get_historical_klines("ETHUSDT", "1h", "19 september 2021")
df = pd.DataFrame(klinest, columns=["timestamp", "open", "high", "low", "close",
                                    "volume", "close_time","quote_av", "trades", "tb_base_av", "tb_quote_av", "ignore"])

del df["close_time"]
del df["quote_av"]
del df["trades"]
del df["tb_base_av"]
del df["tb_quote_av"]
del df["ignore"]

df["open"]= pd.to_numeric(df["open"])
df["high"]= pd.to_numeric(df["high"])
df["low"]= pd.to_numeric(df["low"])
df["close"]= pd.to_numeric(df["close"])
df["volume"]=pd.to_numeric(df["volume"])

df = df.set_index(df["timestamp"])
df.index = pd.to_datetime(df.index, unit="ms")
del df["timestamp"]


df["SMA200"] = ta.trend.sma_indicator(df["close"], 200)
df["SMA600"] = ta.trend.sma_indicator(df["close"], 600)
#print(df)

usdt = 1000
btc =0
lastIndex = df.first_valid_index()

for index, row in df.iterrows():
    if df["SMA200"][lastIndex] > df["SMA600"][lastIndex] and usdt> 10:
        btc = usdt/ df["close"][index]
        btc = btc - 0.007* btc
        usdt = 0
        print("buy BTC at", df["close"][index], "$ the", index)

    if df["SMA200"][lastIndex] < df["SMA600"][lastIndex] and btc > 0.0001:
        usdt = btc * df["close"][index]
        usdt = usdt - 0.007 * usdt
        btc = 0
        print("sell BTC at", df["close"][index], "$ the", index)

    lastIndex = index

finalResult = usdt + btc* df["close"].iloc[-1]
print("final result", finalResult, "USDT")
print("buy and hold result", (1000/ df["close"].iloc[0] * df["close"].iloc[-1]), "USDT")
