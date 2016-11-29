import csv
import pandas as pd
import numpy as np

airport = []
rows = []
with open('reducedcost.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == "ORIGIN":
            continue
        if row[0] not in airport:
            airport.append(row[0])
    f.close()

costData = pd.read_csv('reducedcost.csv', index_col = False)

grouped = costData.groupby(['ORIGIN', 'DEST'])

for i, ((source, dest), flights) in enumerate(grouped):
    price = flights['MARKET_FARE'].mean()

    if np.isnan(price):
        continue

    rows.append([source, dest, price])

    if i % 1000 == 0:
        print i, source, dest

print 'Combinations:', i
print 'Flights:', len(rows)

with open('newnewcosts_2.csv', 'w') as w:
    writer = csv.writer(w)
    for row in rows:
        writer.writerow(row)
    w.close()