import csv


sourceAirport = "JFK"
destinationAirport = "MIA"
count = 0
delay = 0
flyingTo = []
connected = []
dataset = []

with open('dataset.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        date = row[0]
        source = row[1]
        destination = row[2]
        cancellation = row[3]
        delay = row[4]
        dataset.append((date, source, destination))
        if source == sourceAirport:
            if destination not in flyingTo:
                flyingTo.append(destination)

# print flyingTo
for row in dataset:
    if row[1] in flyingTo and row[2] == destinationAirport:
        #     print "1."
        if row[1] not in connected:
            connected.append(row[1])

            
print connected


