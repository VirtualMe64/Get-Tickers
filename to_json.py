import json
import pickle
import os

sub_directories = ["Misc", "Stocks Discussion Ticker Count", "WSB Graphing"]
directories = ["Saved Data/" + sub for sub in sub_directories]

for directory in directories:
    for file_path in os.listdir(directory):
        if (file_path.split(".")[1] == "pkl"):
            with open(directory + "/" + file_path, 'rb') as open_file:
                data = pickle.load(open_file)
                with open(directory + "/" + file_path.split(".")[0] + ".json", 'w') as to_json:
                    json.dump(dict(data), to_json, indent=4)