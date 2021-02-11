from ticker_parser import TickerParser
from comment_getter import CommentGetter
from collections import Counter

#TODO Another class to integrate comment_getter and ticket_counter and saving of results

TICKER_BLACKLIST = ["FOR", "DD", "EV", "CEO", "EOD", "RH", "TD", "HUGE", "IT", "AM"]
url = "https://www.reddit.com/r/wallstreetbets/comments/lh3qli/what_are_your_moves_tomorrow_february_11_2021/"

ticker_parser = TickerParser("tickers.csv", TICKER_BLACKLIST)
comment_getter = CommentGetter("keys.json")


n = 0    
updateN = 500
ticker_counter = Counter()

for top_level_comment in comment_getter.get_comments(url).comments.list():
    n += 1
    ticker_parser.parse_tickers(top_level_comment.body, ticker_counter)
    if (n % updateN == 0):
        print(ticker_counter.most_common(30))

print(n)
print(ticker_counter.most_common(20))