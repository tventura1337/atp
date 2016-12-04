import csv
import argparse
from collections import Counter
from datetime import datetime

# Learning class - contains all value iteration methods
class Learning(object):
    """docstring for GraphNode"""
    def __init__(self, model, time = 0, iterations = 5): # performs value iteration
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

        for i in range(iterations):
            newValues = Counter()
            for state in allStates:
                if state == "TERMINAL_STATE":
                    continue

                maxAction = self.computeActionFromValues(state)
                newValues[state] = self.computeQValueFromValues(state, maxAction)
            for state in allStates:
                self.values[state] = newValues[state]
            print i

    def computeQValueFromValues(self, state, action): # computes qvalue from values of an action
        q = 0
        transitionStates = mdp(self.model, state, action)
        for nextState, prob in transitionStates:
            cost = 0
            if state == self.destination:
                cost = self.model.get_cost(self.destination, "TERMINAL_STATE")
            elif (state == self.source) and (nextState == self.destination):
                cost = self.model.get_cost(state, nextState)
            elif (state != self.source) and (nextState == self.destination):
                cost = self.model.get_cost(self.source, state) + self.model.get_cost(state, nextState) - 100
            q += prob * (cost + (self.discount * self.getValue(nextState)))
        return q

    def computeActionFromValues(self, state): # computes best action from action values
        if state == "TERMINAL_STATE":
            return None

        bestValue = float("inf")
        bestAction = None
        possibleActions = self.model.get_possible_actions(state)
        for action in possibleActions:
            if not possibleActions:
                return None
            q = self.getQValue(state, action)

            if (state, action) not in self.qvalues:
                self.qvalues[state, action] = 0
            self.qvalues[state, action] = q

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

    # normalize output on a 0 to 1 scale
    def normalize(self):
        print self.qvalues

        vals = Counter()
        for val in self.qvalues:
            if self.qvalues[val] == -200.0:
                continue
            vals[val] = self.qvalues[val]

        for k in vals.keys():
            self.qvalues[k] = float(vals[k] - min(vals.values()))/(max(vals.values()) - min(vals.values()))
        print self.qvalues

# Route Graph Class - generates the route maps from source airport to destination airport
class RouteMap(object):
    """docstring for GraphNode"""
    def __init__(self, source=None, destination=None):
        super(RouteMap, self).__init__()
        self.connected = []
        self.allAirports = []
        self.source = source
        self.destination = destination
        self.flights = []
        self.costs = {}

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
        
        for row in dataset:
            if (row[0] == self.source) and (row[1] == self.destination):
                self.connected.append(self.destination)
                break
        
        print self.connected

    def estimate_costs(self, dataset): # generate a hash where key = (source, destination) pair and val = cost
        time_start = datetime.now()
        for row in dataset:
            allStates = self.get_all_states()

            if (row[0] in allStates) and (row[1] in allStates):
                self.costs[(row[0], row[1])] = float(row[2])

        allStates = self.get_all_states()
        for state in allStates:
            self.costs[state, state] = 100
        self.costs[self.destination, "TERMINAL_STATE"] = -200
        #print self.costs

    def train(self, dataset): # add flights for this map on big dataset
        for row in dataset:
            if row[0] == "ORIGIN":
                continue
            source = row[0]
            destination = row[1]
            
            if row[3] == "":
                cancelled = 0
            else:
                cancelled = int(float(row[3]))

            if row[2] == "":
                delayed = 0
            else:
                delayed = int(float(row[2]))
            

            
            if (source == self.source and destination in self.connected)\
                or (source in self.connected and destination == self.destination)\
                    or (source == self.source and destination == self.destination):
                flight = Flight(source, destination, cancelled, delayed)
                self.flights.append(flight) ##save into flight class

    def get_all_airports(self, dataset): # retrun all airports
        for row in dataset:
            name = row[1]
            code = row[0]
            if (name, code) not in self.allAirports:
                self.allAirports.append((name, code))

        return self.allAirports

    def get_all_states(self): # get all states in map
        temp = list(self.connected)
        temp.append(self.source)
        if self.destination not in temp:
            temp.append(self.destination)
        return temp

    def get_possible_actions(self, airport): # get possible actions in a state
        if airport == self.source:
            temp = list(self.connected)
            #print "cost", self.costs(self.source, self.destination)
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

# Flight class - class that defines a flight between two airports
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

# function to load data from csv file
def load_data(filepath):
    dataset = []

    with open(filepath, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            parsedRow = []
            for column in row:
                parsedRow.append(column)

            dataset.append((parsedRow))
        f.close()

    dataset.pop(0)
    return dataset

# function to calculate probabilities from source airport to destination airport
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

## USED FOR DEBUGGING
def find(source, destination):
    model_data = load_data('dataset.csv')

    model = RouteMap(source, destination)
    model.create(model_data)

    print "Training Model"
    model.train(model_data)
    print "Model is trained"
    model_data = None

    cost_data = load_data('costs.csv')
    print "Finding Costs"
    model.estimate_costs(cost_data)
    print "Costs are found"
    cost_data = None

    print "Running value iteration"
    learn = Learning(model)
    print "Finished learning"

    action = learn.getAction(source)
    if not action:
        print "No routes found"
        json = {
            "found": "No"
        }
        return json
    print "Best airport is:" + action
    print "number of flights in analyzed: ", Flight.flightCount

    routes = []
    direct = None
    codename = {}

    code_data = load_data('nameset.csv')
    airports = model.get_all_airports(code_data)
    code_data = None

    for name, code in airports:
        codename[code] = name

    for c in model.connected:
        if (source, c) in learn.qvalues and (c, destination) in learn.qvalues:
            routes.append({
                'name': codename[c],
                'second': round(learn.qvalues[(c, destination)], 3),
                'first': round(learn.qvalues[(source, c)], 3)
            })
    if (source, destination) in learn.qvalues:
        direct = "Direct flight: "+ str(round(learn.qvalues[(source, destination)], 3))

    sortedRoutes = sorted(routes, key=lambda route: route["first"])
    print sortedRoutes

    # for qval in learn.qvalues.keys():
    #     for connect in model.connected:
    #         if qval[0] == connected:
    #
    #     if (qval[0] in model.connected) or (qval[1] in model.connected):
    #         print qval
    json = {
            "found": "yes",
            "source": model.source,
            "destination": model.destination,
            "optimal": codename[action],
            "routes": sortedRoutes,
            "direct": direct,
            "flightNum": Flight.flightCount
            }
    #rt = model.get_specific_flights("BOS", "MIA")

    return json

def airports_list():
    kList = RouteMap()
    code_data = load_data('nameset.csv')
    airports = kList.get_all_airports(code_data)
    response = [{"name": name +" - "+ code, "code": code} for name, code in airports]
    json = {
            "status": "ok",
            "data": response
            }
    return json

def main():
    find("ABQ", "LAX")
    #airports_list()
    pass

if __name__ == "__main__":
    main()
