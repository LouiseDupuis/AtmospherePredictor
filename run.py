from stade_model import StadeModel


num_agents = 100
num_steps = 10

model = StadeModel(num_agents, height = 10, width = 10)

for i in range(num_steps):
    model.step()