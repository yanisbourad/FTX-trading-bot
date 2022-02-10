from coin import coin
from strategie import strategie
class portefeuille:
    def __init__(self, usdt):
        self.usdt = usdt
        #self.balance = balance
        self.monnaies = {}

    def getBalance(self, coin):
        finalResult = self.usdt + self.monnaies[coin] * coin.getDataframeCoin()["close"].iloc[-1]
        print("final result", finalResult, "USDT")

    def getHoldBalance(self,coin):
        print("buy and hold result", (1000 / coin.getDataframeCoin()["close"].iloc[0] * coin.getDataframeCoin()["close"].iloc[-1]), "USDT")
