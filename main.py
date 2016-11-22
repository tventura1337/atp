import csv
import argparse

class Learning(object):
    """docstring for GraphNode"""
    def __init__(self, arg, alpha=0.5, epsilon=0.5):
        super(GraphNode, self).__init__()
        self.flights = arg
        self.airport = None
        self.discount = discount
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)

    def update(self, state, action, nextState, reward):
        oldQValue = self.getQValue(state, action)
        nextQValue = self.getValue(nextState)
        sample = reward + (self.discount * nextQValue)

        self.qValues[state, action] = (1 - self.alpha) * oldQValue + self.alpha * sample

    def computeValueFromQValues(self, state):
        # compute max action q Value
        pass

    def computeActionFromQValues(self, state):
        # compute best Action in state
        pass

    def getAction(self, state):
        # some way to determine where a plane can travel
        pass

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues

    def getQValue(self, state, action):
        return self.qValues[state, action]


class RouteMap(object):
    """docstring for GraphNode"""
    def __init__(self, source=None, destination=None):
        super(RouteMap, self).__init__()
        self.connected = []
        self.source = source
        self.destination = destination
        self.flights = []
        

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

    def train(self, dataset): # add flights for this map on big dataset
        for row in dataset:
            source = row[1]
            destination = row[2]
            delayed = row[4]

            if (source == self.source and destination in self.connected)\
                or (source in self.connected and destination == self.destination)\
                    or (source == self.source and destination == self.destination):
                flight = Flight(source, destination, delayed)
                self.flights.append(flight) ##save into flight class

    def get_all_airports(self, dataset):
        allAirports = []
        for row in dataset:
            name = row[1]
            code = row[0]
            if (name, code) not in allAirports:
                allAirports.append((name, code))
        
        return allAirports
        
    def get_flights(self):
        return self.flights

    def get_routes(self):
        return self.connected
    
    def get_specific_flights(self, airport1, airport2):
        specificFlight = []
        for flight in self.flights:
            if flight.find_a_flight(airport1, airport2):
                specificFlight.append(flight)
        return specificFlight
            

class Flight(object):
    flightCount = 0
    def __init__(self, source, destination, delayed):
        super(Flight, self).__init__()
        self.airport1 = source
        self.airport2 = destination
        self.distance = 0
        self.delayed = delayed
        self.cancelled = None
        
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
    #print model.get_flights()
    #print model.get_specific_flights("JFK", "MIA")
    # flights = model.get_specific_flights("JFK", "MIA")
    # print flights[0].flightCount
    

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

def find(source = "JFK", destination="MIA"):
    
    model = RouteMap(source, destination)
    model_data = load_data('dataset.csv')
    model.create(model_data)

    #real_data = load_data('dataset.csv')
    model.train(model_data)

    # route = {
    #         "source": model.source,
    #         "destination": model.destination,
    #         "routes": model.get_specific_flights("BOS", "MIA")
    #         }
    # rt = model.get_specific_flights("BOS", "MIA")
    mdp(model, source, destination)
    return model


def airports_list():
    model_data = load_data('small_set.csv')
    kList = RouteMap()
    airports = kList.get_all_airports(model_data)
    response = [{"name": name +" - "+ code, "code": code} for name, code in airports]
    json = {"status": "ok",
            "data": response
            }
    return json
if __name__ == "__main__":
    find()
