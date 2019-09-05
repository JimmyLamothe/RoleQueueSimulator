from Player import Player
from utilities import rank, role

class Population():
    player_list = []
    tank_list = []
    dps_list = []
    support_list = []
    SR_list = []
    average_SR = 2200
    max_SR = 2200
    min_SR = 2200
    bronze_list = []
    silver_list = []
    gold_list = []
    platinum_list = []
    diamond_list = []
    master_list = []
    GM_list = []
    top_500_min = None #Top 500 only generated if more than 500 GMs
    top_500_list = []

    def __init__(self, size):
        for i in range(size):
            self.player_list.append(Player())
        for player in self.player_list:
            if player.tank:
                self.tank_list.append(player)
            if player.dps:
                self.dps_list.append(player)
            if player.support:
                self.support_list.append(player)
        for player in self.player_list:
            SR = player.SR
            if SR > self.max_SR:
                self.max_SR = SR
            if SR < self.min_SR:
                self.min_SR = SR
            self.SR_list.append(SR)
            player_rank = rank(SR)
            if player_rank == 'BRONZE':
                self.bronze_list.append(player)
            elif player_rank == 'SILVER':
                self.silver_list.append(player)
            elif player_rank == 'GOLD':
                self.gold_list.append(player)
            elif player_rank == 'PLATINUM':
                self.platinum_list.append(player)
            elif player_rank == 'DIAMOND':
                self.diamond_list.append(player)
            elif player_rank == 'MASTER':
                self.master_list.append(player)
            elif player_rank == 'GM':
                self.GM_list.append(player)
            else:
                print('INVALID SR, please bug check')
                raise Exception
        self.average_SR = int(sum(self.SR_list) / len(self.SR_list))
        self.SR_list = sorted(self.SR_list)
        if len(self.GM_list) > 500:
            self.top_500_min = self.SR_list[-500]
            for player in self.GM_list:
                if player.SR >= self.top_500_min:
                    self.top_500_list.append(player)
                
    def __repr__(self):
        population_string = 'Player count: ' + str(len(self.player_list))
        tank_string = 'Tanks: ' + str(len(self.tank_list))
        dps_string = 'DPS: ' + str(len(self.dps_list))
        support_string = 'Supports: ' + str(len(self.support_list))
        bronze_string = 'Bronze: ' + str(len(self.bronze_list))
        silver_string = 'Silver: ' + str(len(self.silver_list))
        gold_string = 'Gold: ' + str(len(self.gold_list))
        platinum_string = 'Platinum: ' + str(len(self.platinum_list))
        diamond_string = 'Diamond: ' + str(len(self.diamond_list))
        master_string = 'Master: ' + str(len(self.master_list))
        GM_string = 'GM: ' + str(len(self.GM_list))
        top_500_string = ''
        if self.top_500_min:
            top_500_string = 'Top 500 cutoff: ' + str(self.top_500_min)
        average_SR_string = 'Average SR: ' + str(self.average_SR)
        max_SR_string = 'Max SR: ' + str(self.max_SR)
        min_SR_string = 'Min SR: ' + str(self.min_SR)
        return '\n'.join([population_string, tank_string, dps_string,
                          support_string, bronze_string, silver_string,
                          gold_string, platinum_string, diamond_string,
                          master_string, GM_string, top_500_string,
                          average_SR_string, max_SR_string, min_SR_string])
                              
test_population = Population(100000)

print(test_population)
