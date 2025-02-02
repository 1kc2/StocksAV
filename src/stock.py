import os, requests, math, json

class Stock:
    
    def __init__(self, symbol, date):
        # Set symbol, date
        self.symbol = symbol
        self.date = date

        # Get alphavantage key from ENV
        if os.environ.get("ALPHAVANTAGE_API_KEY"):
            self.alphavantage_api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
        else:
            raise EnvironmentError("Must set ALPHAVANTAGE_API_KEY")
        
        # Get daily data
        self.daily_data = self.get_daily_data()

    def get_daily_data(self):
        # Get daily prices of stock for past 200 days
        request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={0}&apikey={1}".format(self.symbol, self.alphavantage_api_key)
        r = requests.get(request_url)
        if r.status_code != 200:
            return False
        
        # Get data from json of successful request
        return r.json()["Time Series (Daily)"]

    def current_price(self):
        # Get current price of stock (realtime)
        request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={0}&interval=1min&apikey={1}".format(self.symbol, self.alphavantage_api_key)
        r = requests.get(request_url)
        if r.status_code != 200:
            return False

        # Return most recent data
        for key, value in r.json()["Time Series (1min)"].items():
            return float(value["4. close"])

    def get_moving_average(self, timeperiod):
        # Get moving average of a stock over a given time period
        url = "https://www.alphavantage.co/query?function=SMA&symbol="+self.symbol+"&interval=daily&time_period="+str(timeperiod)+"&series_type=low&apikey="+self.alphavantage_api_key
        data = requests.get(url)
        return data.json()["Technical Analysis: SMA"][self.date]["SMA"]

    def get_macd_line(self, timeperiod, type): 
        #gets either the macd line or the signal line depending on type
        url = "https://www.alphavantage.co/query?function=MACD&symbol="+self.symbol+"&interval=daily&series_type=open&fastperiod=10&apikey="+self.alphavantage_api_key
        r = requests.get(url)
        if(type=="macd"): 
            return r.json()["Technical Analysis: MACD"][timeperiod]["MACD"] 
        else: 
            return r.json()["Technical Analysis: MACD"][timeperiod]["MACD_Signal"]
