from os import DirEntry
import random
from typing import Counter
from mesa import Agent, model
import math
import numpy

class Car(Agent):
    def __init__(self, unique_id, model, dest):
        super().__init__(unique_id, model)
        self.destination = dest
        self.direction = self.pos
        self.oldPos = self.pos
        
    def move(self):
        road = self.pos

        for agent in self.model.grid.get_cell_list_contents(self.direction):
            if isinstance(agent,Destination):
                print("destination reached")
                road=self.direction
            elif isinstance(agent,Traffic_Light) and agent.state==True:
                road=self.direction
            if isinstance(agent,Traffic_Light) and agent.state==False:
                break
            if len(self.model.grid.get_cell_list_contents(self.direction))>=2:
                break
            if isinstance(agent,Car) and agent.pos==self.direction:
                break

            else : road = self.direction
        # choice = random.choice(road)
        self.oldPos=self.pos
        self.model.grid.move_agent(self, road)

        if self.pos==self.destination.pos:
            print ("destiny reached")
        

    def step(self):

        if self.pos == self.destination.pos:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return

        tmp_vector = (self.destination.pos[0]-self.pos[0], self.destination.pos[1]-self.pos[1])
        magnitud = (math.sqrt(tmp_vector[0]**2+tmp_vector[1]**2))
        vector = (tmp_vector[0]/magnitud,tmp_vector[1]/magnitud)

        results = []

        vectoresEje = ((-1,0),(1,0),(0,1),(0,-1))
        for v in vectoresEje:
            paso = math.acos((v[0]*vector[0])+(v[1]*vector[1]))
            if v == (-1,0):results.append((paso, "Left"))
            elif v == (1,0):results.append ((paso, "Right"))
            elif v == (0,1):results.append ((paso, "Up"))
            elif v == (0,-1):results.append ((paso, "Down"))

        results.sort(key=lambda x:x[0])

        possible_steps = self.model.grid.get_neighborhood(self.pos,moore=False,include_center=False)

        print (self.destination.pos)
        print (results)
        directions = [("Left",0),("Right",3),("Up",2),("Down",1)]

        for r in results:

            for pos in possible_steps:
                if pos==self.destination.pos:
                    self.direction = pos
                    self.model.grid.move_agent(self, pos)
                    return
            dir = r[1]
            cell = None
            route = False;

            for i in directions:
                if dir == i[0]:
                    cell = i[1]
                    break

            for agent in self.model.grid.get_cell_list_contents(possible_steps[cell]):
                # if isinstance(agent,Destination) and agent.pos == self.destination.pos:
                if isinstance(agent,Obstacle) or isinstance(agent,Origin) or isinstance(agent,Destination) or isinstance(agent,Car):
                    pass

                elif isinstance(agent,Road):
                    if (agent.direction == "Down"and dir =="Up" or 
                    agent.direction == "Up"and dir =="Down" or 
                    agent.direction == "Left"and dir =="Right" or
                    agent.direction == "Right"and dir =="Left"):
                        pass
                    else:
                        self.direction= possible_steps[cell]
                        route =True
                
                elif isinstance(agent,Traffic_Light):
                    if agent.state==True:
                        self.direction = possible_steps[cell]
                        route =True
                    else :
                        self.direction = self.pos
                        route =True
                        pass
                        break

            if route==True:
                
                if self.direction==self.oldPos:
                    route==False
                else:
                    break 
            else: continue
            
        self.move()

class Traffic_Light(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        pass

class Destination(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Origin(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def spawn(self, count):
        possible_steps = self.model.grid.get_neighborhood(self.pos,moore=False,include_center=False)
        road = []

        for pos in possible_steps:
            for agent in self.model.grid.get_cell_list_contents(pos):
                if (isinstance(agent,Road) and not isinstance(agent,Car)):
                    road.append(pos)
        choice = random.choice(road)
        return choice

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
