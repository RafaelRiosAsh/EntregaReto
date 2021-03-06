from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json
import random
# import schedule
# import time

class TrafficModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self):

        dataDictionary = json.load(open("mapDictionary.txt"))

        with open('base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            self.cars = 0
            self.instanced_cars= 0

            self.grid = MultiGrid(self.width, self.height,torus = False) 
            self.schedule = RandomActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                    elif col == "#":
                        agent = Obstacle(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "D":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "O":
                        agent = Origin(f"o{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

        self.running = True

    def count_cars(self):
        tmp_count = 0
        for agents, x, y in self.grid.coord_iter():
            for agent in agents:
                if isinstance(agent, Car):
                        tmp_count += 1
        self.cars= tmp_count

    def find_destination(self):
        destinations = []
        for agents, x, y in self.grid.coord_iter():
            for agent in agents:
                if isinstance(agent, Destination):
                        destinations.append(agent)
        chosen_d = random.choice(destinations)
        return chosen_d

    def instance_car(self):
        origin = []
        for agents, x, y in self.grid.coord_iter():
            for agent in agents:
                    if isinstance(agent, Origin):
                            origin.append(agent)
        
        ori = random.choice(origin)
        spawner=ori.spawn(self.cars)

        dest= self.find_destination()

        id_car = self.instanced_cars+1000
        new_car = Car(id_car,self,dest)
        print ("destination",dest.pos)
        self.schedule.add(new_car)
        self.grid.place_agent(new_car, spawner)

        self.instanced_cars+=1

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        
        self.count_cars()

        if self.schedule.steps % 10 == 0: 
            self.instance_car()
            for agents, x, y in self.grid.coord_iter():
                for agent in agents:
                    if isinstance(agent, Traffic_Light):
                        agent.state = not agent.state

            # print(self.count_type())

            # origin[ran].spawn(self.cars)