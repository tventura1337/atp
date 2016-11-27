import csv
import pandas as pd
import argparse
from collections import Counter

class Learning(object):
    """docstring for GraphNode"""
    def __init__(self, model, time = 0, iterations = 100):
        if time:
            self.discount = 0.8
        else:
            self.discount = 1
        self.model = model
        self.iterations = iterations
        self.values = Counter()

        allStates = self.model.get_all_states()
        for i in range(iterations):
            newValues = Counter()
            for state in allStates:
                allActions = self.model.get_possible_actions(state)
                bestValue = float("inf")
                for action in allActions:
                    sumTransitionStates = 0
                    transitionStates = mdp(self.model, state, action)
                    for nextState, prob in transitionStates:
                        if len(nextState) > 3:
                            sumTransitionStates += prob * (1000 + (self.discount * self.getValue(action)))
                        else:
                            sumTransitionStates += prob * (self.model.get_cost(state, nextState) + (self.discount * self.getValue(nextState)))
                    if sumTransitionStates is min(sumTransitionStates, bestValue):
                        bestValue = sumTransitionStates
                        newValues[state] = bestValue
            self.values = newValues

    def computeQValueFromValues(self, state, action):
        q = 0
        transitionStates = mdp(self.model, state, action)

        for nextState, prob in transitionStates:
            if len(nextState) > 3:
                q += prob * (1000 + (self.discount * self.getValue(action)))
            else:
                q += prob * (self.model.get_cost(state, nextState) + (self.discount * self.getValue(nextState)))
        return q

    def computeActionFromValues(self, state):
        bestValue = float("inf")
        bestAction = None
        possibleActions = self.model.get_possible_actions(state)

        for action in possibleActions:
            if not possibleActions:
                return None

            q = self.getQValue(state, action)

            print "Action is: " + action
            print "Value is: " + str(q)

            if q is min(q, bestValue):

                bestValue = q
                bestAction = action

        return bestAction

    def getValue(self, state):
        if state == "cancelled" or state == "delayed":
            return -10
        else:
            return self.values[state]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class RouteMap(object):
    """docstring for GraphNode"""
    def __init__(self, source=None, destination=None):
        super(RouteMap, self).__init__()
        self.connected = []
        self.source = source
        self.destination = destination
        self.flights = []
        self.costs = {}

    def create(self, dataset): # create map of flights on small dataset
        flyingTo = []

        for row in dataset:
            if row[1] == self.source:
                if row[2] not in flyingTo:
                    flyingTo.append(row[2])

        for row in dataset:
            if row[1] in flyingTo and row[2] == self.destination:
                if row[1] not in self.connected:
                    self.connected.append(row[1])

    def estimate_costs(self):
        costData = pd.read_csv('costs.csv', index_col = False)
        for source in self.get_all_states():
            src = costData['ORIGIN'] == source
            allDestinations = self.get_possible_actions(source)
            for destination in allDestinations:
                cost = 0.0
                count = 0
                dst = costData['DEST'] == destination
                tot = costData[src & dst]
                count = len(tot.index)
                cost = tot['MARKET_FARE'].sum()
                if cost == count == 0:
                    avg = 0
                else:
                    avg = cost/count
                self.costs[(source, destination)] = avg
            #    print source + " to " + destination + " is " + str(self.costs[(source, destination)])

    def train(self, dataset): # add flights for this map on big dataset
        for row in dataset:
            source = row[1]
            destination = row[2]
            delayed = row[4]

            if row[3] != "":
                cancelled = int(float(row[3]))
            if row[4] != "":
                delayed = int(float(row[4]))

            if (source == self.source and destination in self.connected)\
                or (source in self.connected and destination == self.destination)\
                    or (source == self.source and destination == self.destination):
                flight = Flight(source, destination, cancelled, delayed)
                self.flights.append(flight) ##save into flight class
        self.estimate_costs()

    def get_all_airports(self, dataset):
        allAirports = []
        for row in dataset:
            name = row[1]
            code = row[0]
            if (name, code) not in allAirports:
                allAirports.append((name, code))

        return allAirports

    def get_all_states(self):
        temp = list(self.connected)
        temp.append(self.source)
        if self.destination not in temp:
            temp.append(self.destination)
        return temp

    def get_possible_actions(self, airport):
        if airport == self.source:
            temp = list(self.connected)
            if self.destination not in temp:
                temp.append(self.destination)
            return temp
        elif airport == self.destination:
            return []
        else:
            temp = self.destination
            return [temp]

    def get_flights(self):
        return self.flights

    def get_routes(self):
        return self.connected

    def get_all_costs(self):
        return self.costs

    def get_cost(self, source, destination):
        return self.costs[(source, destination)]

    def get_specific_flights(self, airport1, airport2):
        specificFlight = []
        for flight in self.flights:
            if flight.find_a_flight(airport1, airport2):
                specificFlight.append(flight)
        return specificFlight

class Flight(object):
    flightCount = 0
    def __init__(self, source, destination, cancelled, delayed):
        super(Flight, self).__init__()
        self.airport1 = source
        self.airport2 = destination
        self.distance = 0
        self.delayed = delayed
        self.cancelled = cancelled
        self.costs = {}

        Flight.flightCount += 1

    def find_a_flight(self, airport1, airport2):
        if(self.airport1 == airport1) and (self.airport2 == airport2):
            return True
        return False

def load_data(filepath):
    dataset = []

    with open(filepath, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            parsedRow = []
            for column in row:
                parsedRow.append(column)

            dataset.append((parsedRow))

    dataset.pop(0)
    return dataset

def mdp(model, source, destination):
    ##example for delayed and cancelled
    flights = model.get_specific_flights(source, destination)
    flightsNum, delayedNum, cancelledNum = 0, 0, 0

    for flight in flights:
        flightsNum += 1
        if flight.delayed:
            delayedNum +=1
        if flight.cancelled:
            cancelledNum += 1

    if flightsNum == 0:
        flightsNum += 1
    delayedProb = delayedNum/float(flightsNum)
    cancelledProb = cancelledNum/float(flightsNum)
    noProb = 1 - (delayedProb + cancelledProb)

    return [(destination, noProb), ("cancelled", cancelledProb), ("delayed", delayedProb)]

def find(source, destination):
    model = RouteMap(source, destination)
    model_data = load_data('dataset.csv')
    model.create(model_data)

    #real_data = load_data('dataset.csv')
    print "Training Model"
    model.train(model_data)
    print "Model is trained"

    print "Running value iteration"
    learn = Learning(model)
    print "Finished learning"

    action = learn.getAction(source)
    print "Best airport is:" + action

    # route = {
    #         "source": model.source,
    #         "destination": model.destination,
    #         "routes": model.get_specific_flights("BOS", "MIA")[0].flightCount
    #         }
    # rt = model.get_specific_flights("BOS", "MIA")
    # return route


def airports_list():
    model_data = load_data('small_set.csv')
    kList = RouteMap()
    airports = kList.get_all_airports(model_data)
    response = [{"name": name +" - "+ code, "code": code} for name, code in airports]
    json = {
            "status": "ok",
            "data": response
            }
    return json

def computeCosts(source, destination):
    pass

def main():
    find("JFK", "MIA")

if __name__ == "__main__":
    main()
