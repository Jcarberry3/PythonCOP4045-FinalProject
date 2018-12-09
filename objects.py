#Objects module

class Item:
    def __init__(self, name="", cost=0.0):
        self.name = name
        self.cost = float(cost)
        #print(str(name) + ", " + str(cost)) #debugging
