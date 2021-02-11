import csv
from collections import Counter

class TickerParser:
    def __init__(self, ticker_csv_path, ticker_blacklist = [], min_len = 2):
            """
            Creates a ticker parser instance
            
            :param ticker_csv_path: Path to csv with tickers as first entry in each row https://www.nasdaq.com/market-activity/stocks/screener\n
            :param ticker_blacklist: Blackist for common all caps words which aren't stock mentions. Default = []\n
            :param min_len: Minimum length for tickers, should usually be 2. Default = 2
            """
            self.ticker_csv_path = ticker_csv_path
            self.ticker_blacklist = ticker_blacklist
            self.min_len = min_len
            self.__generate_ticker_list()
    
    def __generate_ticker_list(self):
        """
        Private methods to generate a list of all tickers from a csv file
        """
        with open(self.ticker_csv_path) as rawTickers:
            csvReader = csv.reader(rawTickers)
            tickers = []
            for row in csvReader:
                ticker = row[0]
                if not (ticker in self.ticker_blacklist or len(ticker) < self.min_len):
                    tickers.append(ticker)

            tickers.pop(0)
        
        self.tickers = tickers

    def parse_tickers(self, string, ticker_counter):
        """
        Finds all tickers in a string and increments a counter once if it appears in the string

        :param string: String to find tickers in.\n
        :param ticker_counter: Counter variable to increment for each ticker found. Type = collections.Counter
        """
        if string.isupper(): # Ignore all caps strings
            return

        for ticker in self.tickers:
            if " " + ticker +  " " in string or "$" + ticker + " " in string or " " + ticker +  "," in string or " " + ticker +  "." in string :
                ticker_counter[ticker] += 1
