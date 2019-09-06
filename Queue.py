from Game import Game

class Queue():
    waiting_room = [] #contains multiple copies of players queuing for multiple roles
    active_games = []
    time = 0

    def open_game(self, player_list):
        game = Game()
        self.active_games.append(game)
        
    def run_games(self):
        for game in active_games:
            game.current_time += 1
            if game.current_time == game.end_time:
                self.close_game(game)

    def close_game(self):
        self.active_games.pop(game)

    def sort_waiting_room(self):
        self.waiting_room.sort(key=lambda player: player.current_wait_time, reverse=True)

    def advance_queue(self):
        self.time += 1
        self.sort_waiting_room()
        # Following could be used to speed up search
        # SR_waiting_room = sorted(self.waiting_room, key=lambda player: player.match_SR(),
        #                          reverse=True)
        tank_waiting_room = [player for player in self.waiting_room
                             if player.match_role == 'TANK']
        dps_waiting_room = [player for player in self.waiting_room
                            if player.match_role == 'DPS']
        support_waiting_room = [player for player in self.waiting_room
                                if player.match_role == 'SUPPORT']

        import itertools
               
        def validate_roles(player_list):
            tanks = 0
            dps = 0
            supports = 0
            for player in player_list:
                print(player.match_role)
                if player.match_role == 'TANK':
                    tanks += 1
                if player.match_role == 'DPS':
                    dps += 1
                if player.match_role == 'SUPPORT':
                    supports += 1
                if tanks > 2 or dps > 2 or supports > 2:
                    return False
            return True

        def validate_SR(player_list):
            SR_list = [player.SR for player in player_list]
            max_SR = max(SR_list)
            min_SR = min(SR_list)
            if max_SR - min_SR <= 500:
                return True
            return False

        iteration = 0
        for dps_pair in itertools.combinations(dps_waiting_room[:50],2):
            for support_pair in itertools.combinations(support_waiting_room[:50],2):
                for tank_pair in itertools.combinations(tank_waiting_room[:50],2):
                    combination = dps_pair + support_pair + tank_pair
                    iteration += 1
                    print(iteration)
                    if validate_SR(combination):
                        print(combination)
                        import sys
                        sys.exit(0)
"""        
        for combination in itertools.combinations(self.waiting_room, 6):
            if validate_roles(combination) and validate_SR(combination):
                print(combination)
                break
"""

def test_queue():
    from Population import Population
    import random
    test_population = Population(300)
    for player in test_population.player_list:
        player.current_wait_time = random.randint(0,20)
        role = random.randint(1,3)
        if role == 1:
            player.match_role = 'TANK'
        elif role == 2:
            player.match_role = 'DPS'
        else:
            player.match_role = 'SUPPORT'
    test_queue = Queue()
    test_queue.waiting_room = test_population.player_list
    test_queue.advance_queue()

test_queue()
