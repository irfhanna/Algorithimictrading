from pandas_datareader import data as pdr
from datetime import date
import yfinance as yf
yf.pdr_override() 
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Tickers list
# We can add and delete any ticker from the list to get desired ticker live data
ticker_list=['AAPL','MSFT']
today = date.today()
# We can get data by our choice by giving days bracket
start_date= "2022-06-18"
end_date="2023-07-18"
files=[]
def getData(ticker):
 print (ticker)
 data = pdr.get_data_yahoo(ticker, start=start_date, end=today)
 dataname= ticker+'_'+str(today)
 files.append(dataname)
 SaveData(data, dataname)
 print( vwap(data,ticker))
 

 # Create VWAP function
def vwap(df,ticker):
 v = df['Volume'].values
 tp = (df['Low'] + df['Close'] + df['High']).div(3).values
 df= df.assign(vwap=(tp * v).cumsum() / v.cumsum())
 sma = df['Close'].rolling(9).mean()
 ema = df['Close'].ewm(span=21, adjust=False).mean()
 fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],name=ticker)])

 fig.add_trace(go.Scatter(
    x=df.index,
    y=df['vwap'],
    mode='lines',
    name='vwap', 
    line=dict(color='red',width=2)))
 fig.add_trace(go.Scatter(
    x=df.index,
    y=sma,
    mode='lines',
    name='sma', 
    line=dict(color='blue',width=2)))
 fig.add_trace(go.Scatter(
    x=df.index,
    y=ema,
    mode='lines',
    name='ema', 
    line=dict(color='yellow',width=2)))
 fig.update_layout(
    height=600)
 fig.show()
 return df

# Create a data folder in your current dir.a 
def SaveData(df, filename):
 df.to_csv('./Starter File/'+filename+'.csv')
#This loop will iterate over ticker list, will pass one ticker to get data, and save that data as file.
for tik in ticker_list:
 getData(tik)
for i in range(0,12):
 df1= pd.read_csv('./Starter File/'+ str(files[i])+'.csv')
 print (df1.head())