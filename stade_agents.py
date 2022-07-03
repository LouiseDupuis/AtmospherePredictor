from mesa import Agent

class StadeAgent(Agent):
    """An agent"""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "N"

    def set_state(self, state):
        self.state = state
    
    def step(self):
        #getting the agent's neighbors : 
        neighbors = self.model.grid.get_neighbors(self.pos, True, False)
        

        states = [agent.state for agent in neighbors]
        #if states.count("S") >= len(self.model.grid.get_neighborhood(self.pos, True, False))//2:
        if states.count("S") >= 4:
            self.neighbors_are_shouting = True
        else :
            self.neighbors_are_shouting = False


    def advance(self):
        if self.neighbors_are_shouting:
            self.set_state("S")


class UltraAgent(Agent):
    """An agent who is always in shouting state"""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "S"