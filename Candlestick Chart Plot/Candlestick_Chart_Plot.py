import yfinance as yf
import mplfinance as mpf
import pandas as pd
ticker = input("Enter the stock name: ")
df =yf.download(
ticker,
start='2023-08-01',
end=2024-09-01',
auto_adjust=False
)
df.columns= df.columns.get_level_values(0)
df =df[['Open', 'High', 'Low', 'Close', 'Volume']]
for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df.dropna(inplace=True)
mpf.plot(
    df,
    type='candle', style='charles',
    title=f'{ticker} Candlestick Chart', ylabel='Price', volume=True
)
