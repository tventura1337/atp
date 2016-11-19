import csv
import argparse

class Learning(object):
    """docstring for GraphNode"""
    def __init__(self, arg):
        super(GraphNode, self).__init__()
        self.flights = arg
        self.airport = None
        self.discount = discount

    def computeQValueFromValues(self, currentState, action):
        pass

    def computeBestActionFromValues(self, state):
        pass

    def getPolicy(self, state):
        return self.computeBestActionFromValues(state)

    def getQValue(self, state, action):
        #print "zzz", self.computeQValueFromValues(state, action)
        return self.computeQValueFromValues(state, action)


class RouteMap(object):
    """docstring for GraphNode"""
    def __init__(self, source, destination):
        super(RouteMap, self).__init__()
        self.connected = []
        self.source = source
        self.destination = destination
        self.flights = []

    def create(self, dataset): # create map of flights on small dataset
        flyingTo = []
        for row in dataset:
            if row[0] == self.source:
                if row[1] not in flyingTo:
                    flyingTo.append(row[1])

        for row in dataset:
            if row[0] in flyingTo and row[1] == self.destination:
                if row[0] not in self.connected:
                    self.connected.append(row[0])
        #print self.connected

    def train(self, dataset): # add flights for this map on big dataset
        for row in dataset:
            source = row[0]
            destination = row[1]
            delayed = row[3]

            if (source == self.source and destination in self.connected)\
                or (source in self.connected and destination == self.destination)\
                    or (source == self.source and destination == self.destination):
                flight = Flight()
                flight.source = source
                flight.destination = destination
                flight.delayed = delayed

                self.flights.append(flight)


    def get_routes(self):
        return self.flights

    def get_routes(self):
        return self.connected

class Flight(object):
    def __init__(self, arg = None):
        super(Flight, self).__init__()
        self.arg = arg
        self.source = None
        self.destination = None
        self.distance = 0
        self.delayed = None
        self.cancelled = None

    def get_flight(self):
        pass

    def new_flight(self, source, destination, delayed):
        pass

def load_data(filepath):
    dataset = []
    with open(filepath, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            source = row[1]
            destination = row[2]
            #distance = row[3]
            delay = row[3]
            cancelled = row[4]
            dataset.append((source, destination, delay, cancelled))
    return dataset

def qLearning(flightRoutes):
    pass

def estimateCost(flight):
    src = flight.source
    dest = flight.destination
    cost = 0.0
    count = 0

    with open('costs.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == src and row[1] == dest:
                cost += float(row[2])
                count += 1

    avg = cost/count
    return avg

def find(source, destination):
    #parser = argparse.ArgumentParser()
    # parser.add_argument('-s', '--source')
    # parser.add_argument('-d', '--destination')
    # args = parser.parse_args()


    model = RouteMap(source, destination)
    model_data = load_data('dataset.csv')
    model.create(model_data)

    #real_data = load_data('dataset.csv')
    model.train(model_data)

    route = {
            "source": model.source,
            "destination": model.destination,
            "routes": model.get_routes()
            }

    return route
    #qLearning(model.get_routes)

def main():
    pass

if __name__ == "__main__":
    main()
