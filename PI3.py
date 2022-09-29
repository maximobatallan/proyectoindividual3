import pandas as pd
import streamlit as st
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def get_candlestick_plot(
        df: pd.DataFrame,
        ma1: int,
        ma2: int,
        ticker: str
):

    
    fig = make_subplots(
        rows = 2,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.1,
        subplot_titles = (f'{ticker}', 'Volumen'),
        row_width = [0.3, 0.7]
    )
    
    fig.add_trace(
        go.Candlestick(
            x = df['startTime'],
            open = df['open'], 
            high = df['high'],
            low = df['low'],
            close = df['close'],
            name = 'Candlestick chart'
        ),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Line(x = df['startTime'], y = df[f'{ma1}_ma'], name = f'{ma1} SMA'),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Line(x = df['startTime'], y = df[f'{ma2}_ma'], name = f'{ma2} SMA'),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Bar(x = df['startTime'], y = df['volume'], name = 'Volume'),
        row = 2,
        col = 1,
    )
    
    fig['layout']['xaxis2']['title'] = 'Fecha'
    fig['layout']['yaxis']['title'] = 'Precio'
    fig['layout']['yaxis2']['title'] = 'Volumen'
    
    fig.update_xaxes(
        rangebreaks = [{'bounds': ['sat', 'mon']}],
        rangeslider_visible = False,
    )
    
    return fig



ticker = st.sidebar.selectbox(
    'Ticker to Plot', 
    options = ['BTC', 'ETH','XRP','AVAX','LTC','BCH','AVAX','SOL','MATIC','FTT']
)

days_to_plot = st.sidebar.slider(
    'Days to Plot', 
    min_value = 1,
    max_value = 300,
    value = 120,
)
ma1 = st.sidebar.number_input(
    'Moving Average #1 Length',
    value = 10,
    min_value = 1,
    max_value = 120,
    step = 1,    
)
ma2 = st.sidebar.number_input(
    'Moving Average #2 Length',
    value = 20,
    min_value = 1,
    max_value = 120,
    step = 1,    
)

url = f'https://ftx.com/api/markets/{ticker}/USD/candles?resolution=86400&start=1641006000'


x = requests.get(url)




resp_dict = x.json()


resp_dict= resp_dict['result']

df = pd.DataFrame.from_dict(resp_dict)


new = df["startTime"].str.split("T", n = 1, expand = True)


df["startTime"]= new[0]


df.drop(columns =["time"], inplace = True)



df[f'{ma1}_ma'] = df['close'].rolling(ma1).mean()
df[f'{ma2}_ma'] = df['close'].rolling(ma2).mean()
df = df[-days_to_plot:]


st.plotly_chart(
    get_candlestick_plot(df, ma1, ma2, ticker),
    use_container_width = True,
)