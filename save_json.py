import pickle
import os
import json

DIRECTORY_PATH = "Saved Data/WSB Graphing/"
file_path = "february 01 2021.pkl"

data_set = pickle.load(open(DIRECTORY_PATH + file_path, 'rb'))

x = {}

for pair in data_set:
    x[pair[0]] = pair[1]

with open("Saved Data/JSONS/" + file_path.split(".")[0]+".json", 'w') as outfile:
    json.dump(x, outfile)