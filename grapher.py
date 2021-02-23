import json # Used to load saved files of mentions
import os # Used to identify files in a directory
import matplotlib.pyplot as plt # Used to create the graph

# TODO convert save format to json so you can store the data/sort order

def file_bar_graph(file_path, threshold, title=""):
    """
    Creates bar graph for one set of ticker mentions from a file

    :param file_path: path to json file with ticker mention data
    :param threshold: minimum relative frequency for ticker to be graphed
    :param title: title of graph. Default is none
    """
    with open(file_path, 'r') as open_file:
        data = json.load(open_file)
        bar_graph(data, threshold, title)

def bar_graph(data, threshold, title=""):
    """
    Creates bar graph for one data set of ticker mentions

    :param data: dict of ticker and mentions in form {ticker: mentions, ticker: mentions...}\n
    :param threshold: minimum relative frequency for ticker to be graphed\n
    :param title: title of graph. Default is none
    """
    rel_freq_data = __to_relative_frequency(data)
    tickers = []
    mentions = []

    for ticker in data.keys():
        val = rel_freq_data[ticker]
        if val > threshold:
            tickers.append(ticker)
            mentions.append(rel_freq_data[ticker])

    print(tickers)
    print(mentions)
    plt.bar(tickers, mentions)
    plt.ylabel("Mentions (relative frequency)")
    plt.xlabel("Tickers")
    plt.title(title)

    plt.show()

def ticker_line_graph(directory_path, ticker, title=""):
    """
    Creates line graph for directory of ticker mention files for on especific ticker

    :param file_path: path to json file with ticker mention data
    :param ticker: ticker to track in the line graph
    :param title: title of graph. Default is ticker name
    """
    data_sets = []
    for file_name in os.listdir(directory_path):
        full_path = directory_path + file_name
        with open(full_path, 'r') as open_file:
            data_set = json.load(open_file)

        data_sets.append(__to_relative_frequency(data_set))

    n = 0
    ys = []
    xs = []
    for data_set in data_sets:
        ys.append(n)
        xs.append(data_set.get(ticker, 0))
        n += 1

    plt.plot(ys, xs)
    plt.legend([ticker])
    plt.ylabel("Mentions (relative frequency)")
    plt.xlabel("Days since February 1")
    plt.title(ticker if title == "" else title)
    plt.show()

def line_graph(directory_path, threshold, title=""):
    """
    Creates line graph for directory of ticker mention files. Good for showing
    trends in mentions

    :param file_path: path to json file with ticker mention data
    :param threshold: minimum relative frequency for ticker to be graphed
    :param title: title of graph. Default is none
    """
    # TODO better method of sorting files (besides alphabetical)
    # TODO better y axis
    data_sets = []
    for file_name in os.listdir(directory_path):
        if file_name.split(".")[1] == "json":
            full_path = directory_path + file_name
            with open(full_path, 'r') as open_file:
                data_set = json.load(open_file)

            data_sets.append(__to_relative_frequency(data_set))
    
    tickers = __get_tickers_from_data(data_sets, threshold)
    n = 0
    ys = []
    xs = []
    for data_set in data_sets:
        ys.append(n)
        xs.append([data_set.get(ticker, 0) for ticker in tickers]) # List of value for every ticker, 0 if not found

        n += 1
    
    plt.plot(ys, xs)
    plt.legend(tickers, fontsize='x-small')
    plt.ylabel("Mentions (relative frequency)")
    plt.xlabel("Days since February 1")
    plt.title(title)
    plt.show()

def __get_tickers_from_data(data_sets, threshold):
    """
    Returns all tickers from a data set of relative frequencies
    whose relative frequency is greater than the threshold

    :param data_sets: list of relative frequencies of ticker mentions\n
    :param threshold: minimum relative frequency for ticker to be counted\n
    :returns: list of ticker in data set
    """
    tickers = []
    for data_set in data_sets:
        [tickers.append(ticker) for ticker in data_set.keys() if data_set[ticker] > threshold] # Add all tickers for which the value is greater than the threshold

    tickers = set(tickers)
    return tickers

def __to_relative_frequency(data_set):
    """
    Modifies data_set from number of mentions per ticker to
    relative frequency of each ticker

    :param data_set: dict of ticker and mentions in form {ticker: mentions, ticker: mentions...}
    :returns: relative frequency data set
    """
    total = float(sum(data_set.values())) # Get total of all mentions
    out = {k : v / total for k, v in data_set.items()} # Create new dictionary where each value is divided by the total
    return out

if __name__ == '__main__':
    toGraph = 1
    
    if toGraph == 0:
        file_path = "Saved Data\WSB Graphing\\february 23 2021.json"
        threshold = 0.01
        file_bar_graph(file_path, threshold, "WSB Weekly Thread")
    elif toGraph == 1:
        directory_path = "Saved Data/WSB Graphing/"
        threshold = 0.035
        line_graph(directory_path, threshold, "WSB Discussion Threads")
    elif toGraph == 2:
        directory_path = "Saved Data/WSB Graphing/"
        ticker = "RKT"
        ticker_line_graph(directory_path, ticker.upper())