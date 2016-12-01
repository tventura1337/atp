import csv
import argparse
from collections import Counter
from datetime import datetime

class Learning(object):
    """docstring for GraphNode"""
    def __init__(self, model, time = 1, iterations = 5):
        if time:
            self.discount = 0.8
        else:
            self.discount = 1
        self.model = model
        self.iterations = iterations
        self.qvalues = Counter()
        self.values = Counter()
        self.source = model.source
        self.destination = model.destination

        
        allStates = self.model.get_all_states()
        print allStates
        for i in range(iterations):
            newValues = Counter()

            for state in allStates:
                if state == "TERMINAL_STATE":
                    continue

                maxAction = self.computeActionFromValues(state)
                newValues[state] = self.computeQValueFromValues(state, maxAction)
 
            for state in allStates:               
                self.values[state] = newValues[state]
            print i," ", self.values, self.values[self.destination]
            


    def computeQValueFromValues(self, state, action):
        q = 0
        transitionStates = mdp(self.model, state, action)
        for nextState, prob in transitionStates:
            q += prob * (self.model.get_cost(state, nextState) + (self.discount * self.getValue(nextState)))
        return q

    def computeActionFromValues(self, state):
        if state == "TERMINAL_STATE":
            return None
            
        bestValue = float("inf")
        bestAction = None
        possibleActions = self.model.get_possible_actions(state)
        #print possibleActions
        for action in possibleActions:
            if not possibleActions:
                return None
            q = self.getQValue(state, action)

            #print "Action is: " + action
            #print "Value is: " + str(q)
            if (state, action) not in self.qvalues:
                self.qvalues[state, action] = 0
            self.qvalues[state, action] = q  
            #print "here"
            if q is min(q, bestValue):

                bestValue = q
                bestAction = action
            
            
        
        return bestAction

    def getValue(self, state):

        return self.values[state]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
        
    def normalize(self):
        
        vals = Counter()
        for val in self.qvalues:
            vals[val] = self.qvalues[val]

        for k in vals.keys():
            self.qvalues[k] = float(vals[k])/sum(vals.values())
        print self.qvalues


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

    def estimate_costs(self, dataset):
        time_start = datetime.now()    
        for row in dataset:
            allStates = self.get_all_states()

            if (row[0] in allStates) and (row[1] in allStates):
                self.costs[(row[0], row[1])] = float(row[2])
                
        allStates = self.get_all_states()
        for state in allStates:
            self.costs[state, state] = 0
        self.costs[self.destination, "TERMINAL_STATE"] = -100
                


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
            #print "cost", self.costs(self.source, self.destination)
            if (self.source, self.destination) in self.costs:
                temp.append(self.destination)
            return temp
        elif airport == self.destination:
            return ["TERMINAL_STATE"]
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
    
    return [(destination, noProb), (source, cancelledProb), (destination, delayedProb)]

def find(source, destination):
    model = RouteMap(source, destination)
    model_data = load_data('dataset.csv')
    cost_data = load_data('costs.csv')
    model.create(model_data)

    #real_data = load_data('dataset.csv')
    print "Training Model"
    model.train(model_data)
    print "Model is trained"
    
    print "Finding Costs"
    model.estimate_costs(cost_data)
    print "Costs are found"

    print "Running value iteration"
    learn = Learning(model)
    print "Finished learning"

    action = learn.getAction(source)
    print "Best airport is:" + action
    print learn.qvalues
    
    routes = []
    for c in model.connected:
        if (source, c) in learn.qvalues and (c, destination) in learn.qvalues:
            
            routes.append({
                'first': ((source, c), learn.qvalues[(source, c)]),
                'second': ((c, destination), learn.qvalues[(c, destination)])
                
            })
    print routes
    
    # for qval in learn.qvalues.keys():
    #     for connect in model.connected:
    #         if qval[0] == connected:
    #
    #     if (qval[0] in model.connected) or (qval[1] in model.connected):
    #         print qval
    

    json = {
            "source": model.source,
            "destination": model.destination,
            "optimal": action,
            "routes": learn.qvalues
            }
    #rt = model.get_specific_flights("BOS", "MIA")
    return json


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


def main():
    find("LAX", "SFO")
    pass

if __name__ == "__main__":
    main()
