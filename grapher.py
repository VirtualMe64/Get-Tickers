import pickle # Used to load saved files of mentions
import os # Used to identify files in a directory
import matplotlib.pyplot as plt # Used to create the graph

# TODO convert save format to json so you can store the data/sort order

def file_bar_graph(file_path, threshold, title=""):
    """
    Creates bar graph for one set of ticker mentions from a file

    :param file_path: path to pickle file with ticker mention data
    :param threshold: minimum relative frequency for ticker to be graphed
    :param title: title of graph. Default is none
    """
    with open(file_path, 'rb') as open_file:
        bar_graph(pickle.load(open_file), threshold, title)

def bar_graph(data, threshold, title=""):
    """
    Creates bar graph for one data set of ticker mentions

    :param data: list of ticker and mentions in form [(ticker, mention), (ticker, mention)...]
    :param threshold: minimum relative frequency for ticker to be graphed
    :param title: title of graph. Default is none
    """
    tickers = []
    mentions = []
    
    for pair in __to_relative_frequency(data):
        if (pair[1] > threshold):
            tickers.append(pair[0])
            mentions.append(pair[1] * 100)
    
    plt.bar(tickers, mentions)
    plt.ylabel("Mentions (relative frequency)")
    plt.xlabel("Tickers")
    plt.title(title)

    plt.show()

def ticker_line_graph(directory_path, ticker, title=""):
    """
    Creates line graph for directory of ticker mention files for on especific ticker

    :param file_path: path to pickle file with ticker mention data
    :param ticker: ticker to track in the line graph
    :param title: title of graph. Default is ticker name
    """
    data_sets = []
    for file_name in os.listdir(directory_path):
        full_path = directory_path + file_name
        with open(full_path, 'rb') as open_file:
            data_set = pickle.load(open_file)

        data_sets.append(__to_relative_frequency(data_set))

    n = 0
    ys = []
    xs = []
    for data_set in data_sets:
        ys.append(n)
        found = False
        for pair in data_set:
            if (pair[0] == ticker):
                xs.append(pair[1] * 100)
                found = True
                break   
    
        if (not found):
            xs.append(0)

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

    :param file_path: path to pickle file with ticker mention data
    :param threshold: minimum relative frequency for ticker to be graphed
    :param title: title of graph. Default is none
    """
    # TODO better method of sorting files (besides alphabetical)
    # TODO better y axis
    data_sets = []
    for file_name in os.listdir(directory_path):
        full_path = directory_path + file_name
        with open(full_path, 'rb') as open_file:
            data_set = pickle.load(open_file)

        data_sets.append(__to_relative_frequency(data_set))
    
    tickers = __get_tickers_from_data(data_sets, threshold)
    n = 0
    ys = []
    xs = []
    for data_set in data_sets:
        ys.append(n)
        xs.append([])
        for ticker in tickers:
            found = False
            for pair in data_set:
                if (pair[0] == ticker):
                    xs[n].append(pair[1] * 100)
                    found = True
                    break
            
            if (not found):
                xs[n].append(0)
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
        for pair in data_set:
            if (pair[1] > threshold):
                tickers.append(pair[0])

    tickers = set(tickers)
    return tickers

def __to_relative_frequency(data_set):
    """
    Modifies data_set from number of mentions per ticker to
    relative frequency of each ticker

    :param data_set: List of ticker and mentions in form [(ticker, mention), (ticker, mention)...]
    :returns: relative frequency data set
    """
    total = 0
    for pair in data_set:
        total += pair[1]

    out = [(pair[0], pair[1]/float(total)) for pair in data_set]   
    return out

if __name__ == '__main__':
    toGraph = 2
    
    if toGraph == 0:
        file_path = "Saved Data\WSB Graphing\\february 19 2021.pkl"
        threshold = 0.004
        file_bar_graph(file_path, threshold, "WSB Weekly Thread")
    elif toGraph == 1:
        directory_path = "Saved Data/WSB Graphing/"
        threshold = 0.035
        line_graph(directory_path, threshold, "WSB Discussion Threads")
    elif toGraph == 2:
        directory_path = "Saved Data/WSB Graphing/"
        ticker = "PLTR"
        ticker_line_graph(directory_path, ticker.upper())