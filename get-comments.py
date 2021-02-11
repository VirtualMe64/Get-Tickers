import json
import csv
from collections import OrderedDict
import praw

with open("keys.json") as keys:
    data = json.load(keys)

with open("tickers.csv") as rawTickers:
    csvReader = csv.reader(rawTickers)
    tickers = []
    for row in csvReader:
        tickers.append(row[0])

    tickers.pop(0)


reddit = praw.Reddit(
    client_id = data["clientId"],
    client_secret = data["clientSecret"],
    user_agent = data["userAgent"],
)

subreddit = reddit.subreddit("stocks")

print("-" * 30)

tickerMentions = {}

for submission in subreddit.comments(limit=1000):
    text = submission.body
    for ticker in tickers:
        if " " + ticker +  " " in text:
            if (ticker in tickerMentions.keys()):
                tickerMentions[ticker] += 1
            else:
                tickerMentions[ticker] = 1

sortedMentions = OrderedDict(sorted(tickerMentions.items(), key=lambda t: t[1], reverse=True))
for pair in sortedMentions.items():
    print(f'{pair[0]}: {pair[1]} mention{"s" if pair[1] > 1 else ""}')