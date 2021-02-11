import json
import csv
from collections import OrderedDict
from datetime import datetime
import praw

blacklist = ["FOR", "DD", "A", "EV", "CEO"]

with open("keys.json") as keys:
    data = json.load(keys)

with open("tickers.csv") as rawTickers:
    csvReader = csv.reader(rawTickers)
    tickers = []
    for row in csvReader:
        ticker = row[0]
        if not ticker in blacklist:
            tickers.append(ticker)

    tickers.pop(0)


reddit = praw.Reddit(
    client_id = data["clientId"],
    client_secret = data["clientSecret"],
    user_agent = data["userAgent"],
)

subreddit = reddit.subreddit("investing")

print("-" * 30)

tickerMentions = {}

dates = []

num = 0

for submission in subreddit.new(limit=100):
    num += 1
    text = submission.selftext
    raw_date = submission.created_utc
    date = datetime.utcfromtimestamp(raw_date)
    dates.append(date)
    for ticker in tickers:
        if " " + ticker +  " " in text or "$" + ticker + " " in text:
            if (ticker in tickerMentions.keys()):
                tickerMentions[ticker] += 1
            else:
                tickerMentions[ticker] = 1

sortedMentions = OrderedDict(sorted(tickerMentions.items(), key=lambda t: t[1], reverse=True))

earliestDate = dates[0]
latestDate = dates[0]
for date in dates:
    if (date < earliestDate): earliestDate = date
    if (date > latestDate): latestDate = date

print(f'Mentions in Posts between {earliestDate.strftime("%Y-%m-%d %H:%M:%S")} and {latestDate.strftime("%Y-%m-%d %H:%M:%S")}')
for pair in sortedMentions.items():
    print(f'{pair[0]}: {pair[1]} mention{"s" if pair[1] > 1 else ""}')

print(num)