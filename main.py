from ticker_parser import TickerParser
from comment_getter import CommentGetter
import pickle
import constants
from datetime import datetime, timedelta
from collections import Counter

#TODO Another class to integrate comment_getter and ticket_counter and saving of results
#TODO Use custom class to store stock data, store if BUY, SELL, HOLD, etc. is in the comment

url = "https://www.reddit.com/r/wallstreetbets/comments/likmpp/weekend_discussion_thread_for_the_weekend_of/"
custom_file_name = "Saved Data/Misc/wsb weekend thread"

ticker_parser = TickerParser("tickers.csv", constants.TICKER_BLACKLIST)
comment_getter = CommentGetter("keys.json")

save = True
runs = 50
n = 0
updateN = 0
ticker_counter = Counter()

if runs != None:
    currTime = datetime.now()
    eta = currTime + timedelta(seconds=(2*runs + 5))

    print(f"Starting comment collection at {currTime.strftime('%I:%M %p')}")
    print(f"Expecting to finish getting comments by {eta.strftime('%I:%M %p')}")

for top_level_comment in comment_getter.get_comments(url, runs).comments.list():
    n += 1
    ticker_parser.parse_tickers(top_level_comment.body, ticker_counter)
    if (updateN != 0 and n % updateN == 0):
        print(ticker_counter.most_common(30))

print(f"Finished comment analysis at {datetime.now().strftime('%I:%M %p')}")
print(n)
print(ticker_counter.most_common(40))

if save:
    filePath = custom_file_name if custom_file_name != "" else "Saved Data/WSB Graphing/" + " ".join(url.split('/')[-2].split('_')[-3:]) + ".pkl"
    print("Saving data to " + filePath)
    saveFile = open(filePath, 'wb')
    pickle.dump(ticker_counter.most_common(), saveFile)