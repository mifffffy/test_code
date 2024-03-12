import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Download historical data for BTC-USD
start_date = pd.to_datetime('2018-01-01')
end_date = pd.to_datetime('today')
df = yf.download(tickers='BTC-USD', start=start_date, end=end_date)['Adj Close']

#Use other JSON data
#df = pd.read_json('data/simple.json')['Close']

# Calculate the rolling maximum
roll_max = df.rolling(center=False, min_periods=1, window=365).max()

# Calculate the daily drawdown relative to the max
daily_draw_down = df / roll_max - 1.0

# Calculate the minimum (negative) daily drawdown
max_daily_draw_down = daily_draw_down.rolling(center=False, min_periods=1, window=100).min()

# Plot the results
fig = go.Figure()

fig.add_trace(go.Scatter(x=df.index, y=daily_draw_down, mode='lines', name='Daily drawdown'))
fig.add_trace(go.Scatter(x=df.index, y=max_daily_draw_down, mode='lines', name='Maximum daily drawdown in time-window'))

fig.update_layout(title='Daily Drawdown and Maximum Daily Drawdown Over Time',
                  xaxis_title='Date',
                  yaxis_title='Drawdown',
                  legend=dict(x=0, y=1, traceorder='normal'),
                  showlegend=True,
                  )

fig.show()
