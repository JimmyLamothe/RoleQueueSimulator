from Population import Population

class Server():
    active_population = []
    passive_population = []
    max_SR_range = 100
    tank_times = []
    dps_times = []
    support_times = []

    def __init__(self, size):
        self.population = Population(size)
    
test_server = Server(100000)

print(test_server.population)
print(test_server.population.player_list[0])
