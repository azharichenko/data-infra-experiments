import csv
from datetime import date

import requests

URL = "https://www.palottery.state.pa.us/Custom/uploadedfiles/winning-numbers-history/PastWinningNumbers.ashx"

if __name__ == "__main__":

    with open("data.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["date", "num1", "num2", "num3", "num4", "num5", "num6"])

        for year in range(1977, 2023):
            data = requests.get(URL, params={"g": 35, "y": year}).json()

            for entry in data:
                d = date.fromtimestamp(int(entry["drawingNumberDate"][6:16]))
                writer.writerow([
                    d,
                    entry["drawingNumber1"],
                    entry["drawingNumber2"],
                    entry["drawingNumber3"],
                    entry["drawingNumber4"],
                    entry["drawingNumber5"],
                    entry["drawingNumber6"],
                ])
