import pandas as pd
from datetime import datetime
from yahoo_fin import stock_info as si

dow_tickers = si.tickers_dow()
today = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
today_string = str(today)

def get_trend_lengths(ticker, start_date, end_date):
    df = si.get_data(ticker, start_date, end_date)
    df['pct_change'] = df['adjclose'].pct_change()
    df['pct_change'] = df['pct_change'].fillna(0)
    df['trend'] = df['pct_change'].apply(lambda x: 1 if x >= 0 else -1)
    df['trend_group'] = df['trend'].ne(df['trend'].shift()).cumsum()
    trends = df.groupby(['trend', 'trend_group']).size().reset_index(name='count')
    pos_trends = trends[trends['trend'] == 1]['count']
    neg_trends = trends[trends['trend'] == -1]['count']
    return pos_trends, neg_trends

start_date_str = input("Enter the start date (YYYY-MM-DD): ")
start_date = datetime.strptime(start_date_str, "%Y-%m-%d")


results = []
for ticker in dow_tickers:
    pos_trends, neg_trends = get_trend_lengths(ticker, start_date, datetime.today())
    result = {'Ticker': ticker, 'Positive Trends': round(pos_trends.mean(), 2), 'Negative Trends': round(neg_trends.mean(), 2)}
    results.append(result)
    print("Finished ticker: " + ticker)
df = pd.DataFrame(results)

df.to_csv('dow_jones_trends' + today_string + '.csv', index=False)
