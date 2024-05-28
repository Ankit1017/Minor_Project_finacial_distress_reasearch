import yfinance as yf
import time
import pandas as pd
def compute_diffs(data):
    average_price = (data["Open"] + data["Close"]) / 2
    data["average_price"] = average_price
    
    for interval in range(1, 3):
        data["diff_" + str(interval)] = data["average_price"].pct_change(periods=interval)

    data["tomorrow"] = data["average_price"].pct_change(periods=-1)
    data.dropna(inplace=True)
    
    return data

def get_historical_data(name_of_token: str):
    token = yf.Ticker(name_of_token)
    data = token.history(period='1y')
    data = data[["Open", "Close", "High", "Low"]]
    data = compute_diffs(data)
    print(data)
    data.index = pd.to_datetime(data.index)
    # Set index to datetime index
    # data.index = data.index.strftime("%Y-%m-%d %H:%M:%S")
    
    data_json = data.to_json(orient="index")
    
    # with open(output_file, "w") as f:
    #     f.write(data_json)
    
    return data_json