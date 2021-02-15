import pickle
import os
import matplotlib.pyplot as plt

DIRECTORY_PATH = "Saved Data/WSB Graphing/"

data_sets = []
relative_freq_data_sets = []

def data_set_to_relative_frequency(data_set):
    total = 0
    for pair in data_set:
        total += pair[1]

    out = [(pair[0], pair[1]/float(total)) for pair in data_set]   
    return out  

for file_name in os.listdir(DIRECTORY_PATH):
    full_path = DIRECTORY_PATH + file_name
    data_set = pickle.load(open(full_path, 'rb'))
    data_sets.append(data_set)
    relative_freq_data_sets.append(data_set_to_relative_frequency(data_set))

tickers = []
threshhold = 0.035
for relative_freq_data_set in relative_freq_data_sets:
    for pair in relative_freq_data_set:
        if (pair[1] > threshhold):
            tickers.append(pair[0])
tickers = set(tickers)

n = 0
ys = []
xs = []
for relative_freq_data_set in relative_freq_data_sets:
    ys.append(n)
    xs.append([])
    for ticker in tickers:
        found = False
        for pair in relative_freq_data_set:
            if (pair[0] == ticker):
                xs[n].append(pair[1] * 100)
                found = True
                break
        
        if (not found):
            xs[n].append(0)
   
    n += 1

#plt.scatter(ys, xs)
plt.plot(ys, xs)
plt.legend(tickers, fontsize='x-small')
plt.ylabel("Mentions (relative frequency)")
plt.xlabel("Days since February 1")
plt.show()