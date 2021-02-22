from ticker_parser import TickerParser
from comment_getter import CommentGetter
from grapher import bar_graph, line_graph
import pickle
import constants
from datetime import datetime, timedelta
from collections import Counter

#TODO Change file format to json
#TODO Another class to integrate comment_getter and ticket_counter and saving of results
#TODO Use custom class to store stock data, store if BUY, SELL, HOLD, etc. is in the comment

url = "https://www.reddit.com/r/wallstreetbets/comments/lpzquu/what_are_your_moves_tomorrow_february_23_2021/"
custom_file_name = ""

ticker_parser = TickerParser("tickers.csv", constants.TICKER_BLACKLIST)
comment_getter = CommentGetter("keys.json")

save = True
save_comments = True
if (save_comments):
    comments = []
    save_comments_path = "Saved Data\\Temp\\comments.pkl"

runs = 500
n = 0
updateN = 0
ticker_counter = Counter()

if runs != None:
    currTime = datetime.now()
    eta = currTime + timedelta(seconds=(2*runs + 5))

    print(f"Starting comment collection at {currTime.strftime('%I:%M %p')}")
    print(f"Expecting to finish getting comments by {eta.strftime('%I:%M %p')}")

for top_level_comment in comment_getter.get_comments(url, runs).comments.list():
    #if (top_level_comment.body != "[deleted]"):
    #    print(top_level_comment.author.created_utc)
    n += 1
    ticker_parser.parse_tickers(top_level_comment.body, ticker_counter)
    if (save_comments):
        comments.append(top_level_comment.body)

    if (updateN != 0 and n % updateN == 0):
        print(ticker_counter.most_common(30))

print(f"Finished comment analysis at {datetime.now().strftime('%I:%M %p')}")
print(f"Number of comments analyzed: {n}")
print(ticker_counter.most_common(40))

if save:
    filePath = custom_file_name if custom_file_name != "" else "Saved Data/WSB Graphing/" + " ".join(url.split('/')[-2].split('_')[-3:]) + ".pkl"
    print("Saving data to " + filePath)
    saveFile = open(filePath, 'wb')
    pickle.dump(ticker_counter.most_common(), saveFile)

if save_comments:
    with open(save_comments_path, 'wb') as open_file:
        pickle.dump(comments, open_file)    

DEFAULT_THRESHOLD = 0.01

bar_graph(ticker_counter.most_common(), DEFAULT_THRESHOLD)