import yfinance as yf

global_periods = ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
global_intervals = ("1m", "2m", "5m", "15m", "30m", "1h", "1d", "5d", "1wk", "1mo", "3mo")

class Data:

    # sets initial values for initial text on buttons
    def __init__(self, period="1y", interval="1wk"): # first setup for before a stock has been input
        self.period = period
        self.interval = interval
        self.period_pointer = global_periods.index(period)
        self.interval_pointer = global_intervals.index(interval)

    # ******* potentially change set_period and set_interval to be one function by passing period or interval as a parameter to change whats updated.
    # changes period by incrementing a pointer in an array
    def set_period(self):
        self.period_pointer = (self.period_pointer + 1) % len(global_periods)    # increments pointer and also resets the pointer to 0 if it goes past the length of the tuple

        self.period = global_periods[self.period_pointer] # setting period to be the index

    # changes interval by incrementing a pointer in an array
    def set_interval(self):
        self.interval_pointer = (self.interval_pointer + 1) % len(global_intervals)    # increments pointer and also resets the pointer to 0 if it goes past the length of the tuple

        self.interval = global_intervals[self.interval_pointer]
        #print(self.interval) for debugging

    # sets the stock and runs the get_data function
    def initialise(self, stock):
        self.stock = stock

        self.get_data()
        #self.print_data() #use for debugging, comment out later

    # uses yfinance to retrieve data based on user set stock, period and interval
    def get_data(self):

        try: # tries to gather data for a stock - works if stock ticker is valid, returns error if not
            ticker = yf.Ticker(self.stock) # wont return an error if an incorrect ticker name is used, so the next line is added too
            data = ticker.history(period=self.period, interval=self.interval) # gathers data from the ticker object
            self.date = data.index
            self.open = data["Open"].values  # values formats to array
            self.close = data["Close"].values
            self.high = data["High"].values
            self.low = data["Low"].values
            self.stockname = self.stock
            self.volume = data["Volume"].values
            self.dividends = data["Dividends"].values

        except:
            print("invalid stock ticker")




    # prints data for debugging purposes - same idea can probably be used for formatting the data
    def print_data(self):
            for i in range(len(self.date)): # each set of data should be the same length
                print(f"{self.stockname} {i} {self.date[i]} -- ",
                      f"High: {round(self.high[i], 2)} ",
                      f"Low: {round(self.low[i], 2)} ",   # also round is used to round the data to the nearest 1p (for ease of use)
                      f"Open: {round(self.open[i], 2)} ",
                      f"Close: {round(self.low[i], 2)}")