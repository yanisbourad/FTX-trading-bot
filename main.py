# On import api de binance pour importer les cours du marche
#on import pandas pour gerer les tableaux facilement
#

from binance.client import Client
import pandas as pd
import ta
import matplotlib.pyplot as plt

# on import les resultat du cours du marché du BTCUSDT, a partir du 1 janvier 2021, a chaque une heure
klinest = Client().get_historical_klines("BTCUSDT", "1w", "01 january 2017")
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
print(df)

data= getminute
plt.cla()
plt.plot()
