import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
pio.renderers.default='browser'
import requests




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
    
if __name__ == '__main__':
    
    i = 'BTC'
    #,'XRP','ETH','AVAX','LTC','BCH','AVAX','SOL','MATIC','FTT'





    url = f'https://ftx.com/api/markets/{i}/USD/candles?resolution=86400&start=1641006000'


    x = requests.get(url)




    resp_dict = x.json()


    resp_dict= resp_dict['result']

    df = pd.DataFrame.from_dict(resp_dict)


    new = df["startTime"].str.split("T", n = 1, expand = True)


    df["startTime"]= new[0]


    df.drop(columns =["time"], inplace = True)
    
    df['10_ma'] = df['close'].rolling(10).mean()
    df['20_ma'] = df['close'].rolling(20).mean()
    
    fig = get_candlestick_plot(df, 10, 20,i)
    fig.show()