from ticker_parser import TickerParser
from comment_getter import CommentGetter
import pickle
import constants
from collections import Counter

#TODO Another class to integrate comment_getter and ticket_counter and saving of results
#TODO Use custom class to store stock data, store if BUY, SELL, HOLD, etc. is in the comment

#url = "https://www.reddit.com/r/wallstreetbets/comments/lh3qli/what_are_your_moves_tomorrow_february_11_2021/"

ticker_parser = TickerParser("tickers.csv", constants.TICKER_BLACKLIST)
comment_getter = CommentGetter("keys.json")

save = False
n = 0    
updateN = 0
ticker_counter = Counter()

for top_level_comment in comment_getter.get_comments(url, 50).comments.list():
    n += 1
    ticker_parser.parse_tickers(top_level_comment.body, ticker_counter)
    if (updateN != 0 and n % updateN == 0):
        print(ticker_counter.most_common(30))
    
print(n)
print(ticker_counter.most_common(40))

if save:
    print("Saving data to " + "Saved Data/WSB Graphing/" + " ".join(url.split('/')[-2].split('_')[-3:]) + ".pkl")
    saveFile = open("Saved Data/WSB Graphing/" + " ".join(url.split('/')[-2].split('_')[-3:]) + ".pkl", 'wb')
    pickle.dump(ticker_counter.most_common(), saveFile)