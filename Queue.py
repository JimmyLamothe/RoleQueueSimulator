from Game import Game

class Queue():
    waiting_room = [] #contains multiple copies of players queuing for multiple roles
    active_games = []
    successes = 0
    failures = 0
    SR_range = 200 #Max range of SRs allowed to form a game
    time = 0

    def open_game(self, player_list):
        game = Game(player_list)
        self.active_games.append(game)
        print(game)
        
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
        candidates = self.waiting_room
        # Following could be used to speed up search
        # SR_waiting_room = sorted(self.waiting_room, key=lambda player: player.match_SR(),
        #                          reverse=True)
        selection = candidates[0] #Player we will try to find a match for

        def tank_candidates():
            return [player for player in candidates if player.match_role == 'TANK']

        def dps_candidates():
            return [player for player in candidates if player.match_role == 'DPS']

        def support_candidates():
            return [player for player in candidates if player.match_role == 'SUPPORT']

        def find_match(player, SR_range = 200): #Returns player list or False if no valid SR matches
            SR_range = range(int(player.dps_SR - SR_range / 2), int(player.dps_SR + SR_range / 2))
            dps_list = [player for player in dps_candidates()
                        if player.dps_SR in SR_range]
            tank_list = [player for player in tank_candidates()
                         if player.tank_SR in SR_range]
            support_list = [player for player in support_candidates()
                            if player.support_SR in SR_range]
            if len(dps_list) < 2 or len(tank_list) < 2 or len(support_list) < 2:
                return False
            return dps_list[0:2] + tank_list[0:2] + support_list[0:2]

        def process_queue(selection, SR_range): #TO DO: Establish stop condition
            print(str(len(candidates)))
            print('First 10 current candidates:')
            for player in candidates[0:10]:
                print('Player ' + str(player.ID))
            print('Current candidate:')
            print('Player ' + str(player.ID))
            player_list = find_match(selection, SR_range)
            if player_list:
                self.open_game(player_list)
                for player in player_list:
                    try:
                        print(player in candidates)
                        print('Removing Player ' + str(player.ID))
                        candidates.remove(player)
                        print(player in candidates)
                    except ValueError as e:
                        print('Failed to remove ' + str(player.ID))
                        print('Player info: ')
                        print(player)
                        print('Following players in player_list:')
                        for player in player_list:
                            print('Player ' + str(player.ID))
                        print('First 10 players in candidates:')
                        for player in candidates[0:10]:
                            print('Player ' + str(player.ID))
                        raise e
                selection = candidates[0]
                self.successes += 1
                process_queue(selection, SR_range)
            else:
                candidates.remove(selection)
                self.failures += 1
                selection = candidates[0]
                try:
                    process_queue(selection, SR_range)                               
                except Exception:
                    print('Player: \n' + str(selection))
                    return
        process_queue(selection, self.SR_range)
        print(str(self.successes))
        print(str(self.failures))
        




"""
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
"""        
        for combination in itertools.combinations(self.waiting_room, 6):
            if validate_roles(combination) and validate_SR(combination):
                print(combination)
                break
"""


def test_queue():
    from Population import Population
    import random
    test_population = Population(5000)
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
