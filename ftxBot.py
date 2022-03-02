import ftx
import pandas as pd
import ta
import time
import discord

# Personal information to change
idChannel = None    #int, not string
token = ""
accountName = ''
APIKey = ""
APIsecret = ""

# connect to FTX server
client = ftx.FtxClient(api_key=APIKey,
                   api_secret = APIsecret, subaccount_name=accountName)
# coin data as a dataframe
def df(pairSymbol):
    data = client.get_historical_data(
        market_name=pairSymbol,
        resolution=3600,
        limit=1000,
        start_time=float(
            round(time.time())) - 220 * 3600,
        end_time=float(round(time.time())))
    df = pd.DataFrame(data)
    df['EMA1'] = ta.trend.ema_indicator(close=df['close'], window=7)
    df['EMA2'] = ta.trend.ema_indicator(close=df['close'], window=30)
    df['EMA3'] = ta.trend.ema_indicator(close=df['close'], window=50)
    df['EMA4'] = ta.trend.ema_indicator(close=df['close'], window=100)
    df['EMA5'] = ta.trend.ema_indicator(close=df['close'], window=121)
    df['EMA6'] = ta.trend.ema_indicator(close=df['close'], window=200)
    df['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=14, smooth1=3, smooth2=3)
    del df["time"]
    return df

pd.set_option('display.max_columns', 14)

# get quantity of a coin

def getBalance(myclient, coin):
    jsonBalance = myclient.get_balances()
    if jsonBalance == []:
        return 0
    pandaBalance = pd.DataFrame(jsonBalance)
    #print(pandaBalance)
    if pandaBalance.loc[pandaBalance['coin'] == coin].empty:
        return 0
    else:
        return float(pandaBalance.loc[pandaBalance['coin'] == coin]['total'])

# buying strategy
def buyCondition(row, previousRow):
    if row['EMA1'] > row['EMA2'] and row['EMA2'] > row['EMA3'] and row['EMA3'] > row['EMA4'] and row['EMA4'] > row[
        'EMA5'] and row['EMA5'] > row['EMA6'] and row['STOCH_RSI'] < 0.82:
        return True
    else:
        return False

# selling strategy
def sellCondition(row, previousRow):
    if row['EMA6'] > row['EMA1'] and row['STOCH_RSI'] > 0.2:
        return True
    else:
        return False

# if a coin is not in your balance, add a new line if you want to trade this coin,
# just change the value of the key "coin" with the symbol of the coin, make sure this coin is in FTX

def addCoins():
    newCoin.append({'coin': 'BNB', 'total': 0.0, 'free': 0.0, 'availableWithoutBorrow': 0.0, 'usdValue': 0.0, 'spotBorrow': 0.0})
    newCoin.append({'coin': 'AVAX', 'total': 0.0, 'free': 0.0, 'availableWithoutBorrow': 0.0, 'usdValue': 0.0, 'spotBorrow': 0.0})
    newCoin.append({'coin': 'FTM', 'total': 0.0, 'free': 0.0, 'availableWithoutBorrow': 0.0, 'usdValue': 0.0, 'spotBorrow': 0.0})
    newCoin.append({'coin': 'AAVE', 'total': 0.0, 'free': 0.0, 'availableWithoutBorrow': 0.0, 'usdValue': 0.0, 'spotBorrow': 0.0})
    #make sure we don't have the same coin twice
    for j in jsonBalance:
        for i in newCoin:
            if i["coin"] in j.values():
                newCoin.remove(i)
    # add new coins
    for i in newCoin:
        jsonBalance.append(i)

# find the total value of the wallet
def getValueWallet():
    wallet = 0
    for i in jsonBalance:
        wallet+= i["usdValue"]
    wallet = round(wallet,2)
    return wallet

# function to get notify in your discord's channel
def discordNotification(idChannel, msg, token):
    clientDiscord = discord.Client()
    @clientDiscord.event
    async def on_ready():
        print(f"{clientDiscord.user} has connected to Discord!")
        channel = clientDiscord.get_channel(idChannel)
        await channel.send(msg)
        await clientDiscord.close()
        time.sleep(1)
    clientDiscord.run(token)

if __name__ == '__main__':
    nbPosition = 0          # number of coin you're trading actually
    coinsTrading = []
    notificationList = []
    coins = 4               # max of coin you want to trade
    jsonBalance = client.get_balances()
    newCoin = []
    addCoins()

    for i in jsonBalance:
        # Fiats are not taken into account
        if i["coin"] == "USD" or i["coin"] == "USDT":
            continue
        pair = i["coin"] + "/USD"
        fiatSymbol = 'USD'
        cryptoSymbol = i["coin"]
        print(pair)
        dframe = df(pair)
        print(dframe.iloc[-5::])
        i["position"] = False

        fiatAmount = getBalance(client, fiatSymbol)
        cryptoAmount = getBalance(client, cryptoSymbol)
        actualPrice = df(pair)['close'].iloc[-1]
        minToken = 5 / actualPrice
        print('coin price :', actualPrice, 'usd balance', fiatAmount, 'coin balance :', cryptoAmount)

        # amountOneCoin is the amount available for a coin, we can do 4 trade max
        wallet = getValueWallet()
        amountOneCoin = wallet/ coins
        if i["usdValue"] > 1:
            nbPosition+= 1
            i["position"] = True

        if i["position"] == True:
            coinsTrading.append(i["coin"])

        # buying procedure

        if buyCondition(dframe.iloc[-2], dframe.iloc[-3]):
            if float(fiatAmount) > 12 and i["position"] == False and nbPosition < coins:
                quantityBuy = round(float(amountOneCoin) / actualPrice, 6)
                buyOrder = client.place_order(
                    market=pair,
                    side="buy",
                    price=None,
                    size=quantityBuy,
                    type='market')
                messageBuy = f"BUY {buyOrder}"
                i["position"] = True
                notificationList.append(messageBuy)
            else:
                # print("If you  give me more USD I will buy more", cryptoSymbol)
                messagenoBuy = f"{pair}: don't have enough of USD to buy..."
                notificationList.append(messagenoBuy)

        # selling procedure
        elif sellCondition(dframe.iloc[-2], dframe.iloc[-3]):
            if float(cryptoAmount) > minToken:
                sellOrder = client.place_order(
                    market=pair,
                    side="sell",
                    price=None,
                    size= cryptoAmount,
                    type='market')
                messageSell = f"SELL {sellOrder}"
                i["position"] = False
                notificationList.append(messageSell)

            else:
                messageNoSell = f"{pair}: don't have enough to sell..."
                notificationList.append(messageNoSell)

        # no opportunity
        else:
            messageNothing = f"{pair}: no opportunity"
            notificationList.append(messageNothing)

    coinsTrading = ', '.join(coinsTrading)
    positions = f"number of trade: {nbPosition} ({coinsTrading})"
    notificationList.append(positions)
    msg = '\n'.join(notificationList)

    # post the results on the discord channel
    discordNotification(msg=msg, token= token,
                        idChannel= idChannel)
