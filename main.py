import csv

class learning(object):
    """docstring for GraphNode"""
    def __init__(self, arg = None):
        super(GraphNode, self).__init__()
        self.arg = arg
        self.airport = None
        

        
        
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
                flight.airport1 = source
                flight.airport2 = destination
                flight.delayed = delayed
                
                self.flights.append(flight)
                
    
    def get_routes(self):
        return self.flights
        
        
class Flight(object):
    def __init__(self, arg = None):
        super(Flight, self).__init__()
        self.arg = arg
        self.airport1 = None
        self.airport2 = None
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

def main():
    
    model = RouteMap("JFK", "STL")
    model_data = load_data('dataset.csv')
    model.create(model_data)
    
    #real_data = load_data('dataset.csv')
    model.train(model_data)
    
    qLearning(model.get_routes)


if __name__ == "__main__":
    main()