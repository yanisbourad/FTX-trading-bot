
from coin import coin
import time
from plyer import notification

if __name__ == '__main__':
    btc = coin("BTCUSDT","10 october 2020","1h")
    btc.initializeDataframeCoin()
    df = btc.getDataframeCoin()
    usdt = 1000
    btc = 0
    lastIndex = df.first_valid_index()

    for index, row in df.iterrows():
        if df["SMA200"][lastIndex] > df["SMA600"][lastIndex] and usdt > 10:
            btc = usdt / df["close"][index]
            btc = btc - 0.007 * btc
            usdt = 0
            prixAchat = df["close"][-1]
            print("buy BTC at", df["close"][index], "$ the", index)

        if df["SMA200"][lastIndex] < df["SMA600"][lastIndex] and btc > 0.0001:
            usdt = btc * df["close"][index]
            usdt = usdt - 0.007 * usdt
            btc = 0
            prixVente = df["close"][-1]
            print("sell BTC at", df["close"][index], "$ the", index)

        lastIndex = index

    finalResult = usdt + btc * df["close"].iloc[-1]
    print("final result", finalResult, "USDT")
    print("buy and hold result", (1000 / df["close"].iloc[0] * df["close"].iloc[-1]), "USDT")


