#!/bin/python3

import json
from pprint import pprint

data = []

with open("input.dat") as f:
    data = f.readlines()


date = data[0][:-1]

exercise = ""

for i, point in enumerate(data[2:]):
    if point == "\n":
        exercise += "|"
        continue
    else:
        if point[-1] == "\n":
            exercise += point[:-1]
        else:
            exercise += point
    if i < len(data) - 3:
        if data[2 + i + 1] != "\n":
            exercise += ";"

entry = {"date": date, "exercise": exercise}
pprint(entry)

with open("data.json", "a") as f:
    json.dump(entry, f)
    f.write("\n")
