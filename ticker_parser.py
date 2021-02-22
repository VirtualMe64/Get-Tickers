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
    
    def __has_ticker(self, ticker, string):
        """
        Regex: '\\b{ticker}\\b'.\n
        Returns if a ticker is in a string. This means the ticker is included, and either side of the ticker is either
        the stard/end of the statement or a NON-LETTER character.\n
        So if ticker is "GME", "$GME is cool" returns true but "I like AGME" returns false
        """
        ticker_length = len(ticker)
        string_length = len(string)
        indices = [i for i in range(string_length - ticker_length + 1) if string[i : i + ticker_length] == ticker]
        for i in indices:
            first = False
            second = False
            if i == 0 or not string[i - 1: i].isalpha():
                first = True
            if i + ticker_length == string_length or not string[i + ticker_length : i + ticker_length + 1].isalpha():
                second = True
            if first and second:
                return True

        return False

    def parse_tickers(self, string, ticker_counter):
        """
        Finds all tickers in a string and increments a counter once if it appears in the string

        :param string: String to find tickers in.\n
        :param ticker_counter: Counter variable to increment for each ticker found. Type = collections.Counter
        """
        if string.isupper(): # Ignore all caps strings
            return

        for ticker in self.tickers:
            if ticker in string:
                if self.__has_ticker(ticker, string):
                    ticker_counter[ticker] += 1
