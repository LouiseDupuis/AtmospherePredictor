from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import SingleGrid
from stade_agents import StadeAgent, UltraAgent

class StadeModel(Model):
    """A model with some number of agents."""

    def __init__(self, num_agents = 1, width = 2, height= 2):
        self.running = True

        self.num_agents = num_agents
        # Create agents and scheduler
        self.schedule = SimultaneousActivation(self)

        #creating a grid - for now, default rid
        self.grid = SingleGrid(width, height, True)

        
        for i in range(self.num_agents):
            a = StadeAgent(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            self.grid.place_agent(a, self.grid.find_empty())
            #set the state randomly
            if self.random.random()>0.8:
                a.set_state("S")

    def step(self):
            """Advance the model by one step."""
            self.schedule.step()


