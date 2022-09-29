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
            name = 'Grafico de Velas Japonesas'
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
        go.Line(x = df['startTime'], y = df['lower_band'], name = f'{ma2} banda baja'),
        row = 1,
        col = 1,
    )

    fig.add_trace(
        go.Line(x = df['startTime'], y = df['upper_band'], name = f'{ma2} banda alta'),
        row = 1,
        col = 1,
    )    







    fig.add_trace(
        go.Bar(x = df['startTime'], y = df['volume'], name = 'Volumen'),
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
    'Cryptomonedas', 
    options = ['BTC', 'ETH','XRP','AVAX','LTC','BCH','AVAX','SOL','MATIC','FTT']
)

days_to_plot = st.sidebar.slider(
    'Cantidad de dias a graficar', 
    min_value = 1,
    max_value = 300,
    value = 120,
)
ma1 = st.sidebar.number_input(
    'Media Movil 1',
    value = 10,
    min_value = 1,
    max_value = 120,
    step = 1,    
)
ma2 = st.sidebar.number_input(
    'Media Movil 2',
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
df[f'{ma2}_ma'] = df['close'].rolling(ma2).mean()
df[f'{ma2}_ma'] = df['close'].rolling(ma2).mean()
df['stddev'] = df['close'].rolling(window=20).std()
df['lower_band'] = df[f'{ma1}_ma'] - (2 * df['stddev'])
df['upper_band'] = df[f'{ma1}_ma'] + (2 * df['stddev'])



df["dif"] = df.close.diff()

df["variacion"] = df.dif/df.close.shift(1)*100

df = df[-days_to_plot:]
df.to_csv('btcs')


st.plotly_chart(
    get_candlestick_plot(df, ma1, ma2, ticker),
    use_container_width = True,
)

variacion =round(df.iloc[-1, -1],2)

st.write(f'La Variacion Porcentual diaria de {ticker} sobre el par USD es de: {variacion}%')