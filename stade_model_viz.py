from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from stade_model import StadeModel

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
    }

    if agent.state == "N":
        portrayal["Color"] = "grey"
        # portrayal["Layer"] = 0
    elif agent.state == "S":
        portrayal["Color"] = "red"
        # portrayal["Layer"] = 1
    return portrayal


# ---- Parameters-----
width = 50
height = 15
num_agents = width * height

#----------------------

grid = CanvasGrid(agent_portrayal, width, height, width*10, height*10)
server = ModularServer(
    StadeModel, [grid], "Stade Model", {"num_agents": num_agents, "width": width, "height": height}
)
server.port = 8521  # The default
server.launch()