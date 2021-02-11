import json
import csv
from collections import Counter
import praw
import pickle

#TODO Get comments a few get_mores at a time instead of all at once
#TODO Every thousand new comments, process these new comments and update the file, PRINT something

blacklist = ["FOR", "DD", "EV", "CEO", "EOD", "RH", "TD", "HUGE"]
minLen = 2

with open("keys.json") as keys:
    data = json.load(keys)

with open("tickers.csv") as rawTickers:
    csvReader = csv.reader(rawTickers)
    tickers = []
    for row in csvReader:
        ticker = row[0]
        if not (ticker in blacklist or len(ticker) < minLen):
            tickers.append(ticker)

    tickers.pop(0)

print("Tickers generated")

reddit = praw.Reddit(
    client_id = data["clientId"],
    client_secret = data["clientSecret"],
    user_agent = data["userAgent"],
)

print("Client generated")

save = True
name = "wsbTop"
url = "https://www.reddit.com/r/wallstreetbets/comments/lh3qli/what_are_your_moves_tomorrow_february_11_2021/"
submission = reddit.submission(url=url)
print("Submission accessed")
while True:
    try:
        submission.comments.replace_more(600) # ~300 = 15,000 comments, should take 10 minutes (2s * n)
        break
    except:  
        print("Hey look an error!")  
        sleep(1)

print("Comments replaced")
ticker_counter = Counter()

def get_tickers(comment, counter):
    text = comment.body
    if text.isupper():
        return

    for ticker in tickers:
        if " " + ticker +  " " in text or "$" + ticker + " " in text or " " + ticker +  "," in text or " " + ticker +  "." in text :
            ticker_counter[ticker] += 1

n = 0    
updateN = 1000

for top_level_comment in submission.comments.list():
    n += 1
    get_tickers(top_level_comment, ticker_counter)
    if (n % updateN == 0):
        print(ticker_counter.most_common(30))


if save:
    saveFile = open("Saved Data/Stocks Discussion Ticker Count/" + name + " " + " ".join(url.split('/')[-2].split('_')[-3:]) + ".pkl", 'wb')
    pickle.dump(ticker_counter.most_common(), saveFile)

print(n)
print(ticker_counter.most_common(20))