import matplotlib.pyplot as plt
import pickle

def data_set_to_relative_frequency(data_set):
    total = 0
    for pair in data_set:
        total += pair[1]

    out = [(pair[0], pair[1]/float(total)) for pair in data_set]   
    return out  

file_path = "Saved Data\Misc\wsb weekend thread"
with open(file_path, 'rb') as open_file:
    raw_data = pickle.load(open_file)
    data = data_set_to_relative_frequency(raw_data)

tickers = []
mentions = []
threshold = 0.005

for pair in data:
    if (pair[1] > threshold):
        tickers.append(pair[0])
        mentions.append(pair[1] * 100)

plt.bar(tickers, mentions)
plt.ylabel("Mentions (relative frequency)")
plt.xlabel("Tickers")

plt.show()