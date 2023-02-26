from binance.client import Client
import pandas as pd
import talib as ta


api_key = ""
secret_key = ""
symbol = "BTCBUSD"
leverage = "20"

client = Client(api_key,secret_key)


def ordershort(symbol,amount):
    #short
    client.futures_create_order(symbol=symbol,side='SELL',type='MARKET',quantity=str(amount))

def ordersl_short(symbol,amount,stopPrice):   
    #sl-short
    client.futures_create_order(symbol=symbol,side='BUY',type='STOP_MARKET',stopPrice=float(stopPrice),quantity=str(amount) ,closePosition='true')

def ordercl_short(symbol,amount):
    #close short
    client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=str(amount))

def orderlong(symbol,amount):
    #short
    client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=str(amount))

def ordersl_long(symbol,amount,stopPrice):   
    #sl-long
    client.futures_create_order(symbol=symbol,side='SELL',type='STOP_MARKET',stopPrice=float(stopPrice),quantity=str(amount) ,closePosition='true')

def ordercl_long(symbol,amount):
    #close long
    client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=str(amount))


def main():    
    while True :
        #Load data of candle stock 15m
        data = client.futures_historical_klines(symbol,"15m","2023-01-01",None,1000)
        df=pd.DataFrame(data,columns=["time","open","high","low","close_LP","volume","ct","qav","not","tbv","tbqav","ignore"])

        #Load data of Accounts
        bals=client.futures_account_balance()
        curent_bal=[bal for bal in bals if float(bal['balance'])!=0]
        df_bal=pd.DataFrame(curent_bal,columns=['asset','balance','withdrawAvailable','updateTime'])

        #Load order of accounts 
        positions=client.futures_position_information()
        current_position=[position for position in positions if float(position['positionAmt']) !=0 and position['symbol'] == symbol]
        df_pos=pd.DataFrame(current_position,columns=['symbol','entryPrice','unRealizedProfit','isolatedWallet','positionAmt','positionSide','leverage'])

        #leverage setting
        client.futures_change_leverage(symbol=symbol, leverage = int(leverage))

        #EMA21 and EMA55 strategy
        df['EMA21'] = ta.EMA(df["close_LP"], timeperiod=21)
        df['EMA55'] = ta.EMA(df["close_LP"], timeperiod=55)
        df['PEV_EMA21'] = df['EMA21'].shift(1)
        df['PEV_EMA55'] = df['EMA55'].shift(1)

        df.loc[(df['PEV_EMA21'] < df['EMA55']) & (df['EMA21'] > df['EMA55']),'EMA_Signal'] = 'LONG'
        df.loc[(df['PEV_EMA21'] > df['EMA55']) & (df['EMA21'] < df['EMA55']),'EMA_Signal'] = 'SHORT'


if __name__ == "__main__":
    main()


