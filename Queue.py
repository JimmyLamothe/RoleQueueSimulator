from Game import Game
from utilities import average

class Queue():
    waiting_room = [] #contains multiple copies of players queuing for multiple roles
    active_games = []
    next_game_ID = 0
    successes = 0
    failures = 0
    SR_range = 200 #Max range of SRs allowed to form a game
    time = 0

    def open_game(self, player_list):
        game = Game(player_list, self.next_game_ID)
        self.next_game_ID += 1
        for player in player_list:
            self.waiting_room.remove(player)
            player.current_wait_time = 0
        self.active_games.append(game)
        print(game)
        
    def run_games(self):
        for game in self.active_games:
            game.current_time += 1
            if game.current_time == game.end_time:
                self.close_game(game)

    def close_game(self, game):
        self.active_games.remove(game)
        for player in game.player_list:
            if player.leave_queue():
                pass
            else:
                print('Player ' + str(player.ID) + ' returned to queue')
                self.waiting_room.append(player)
        print('Game ' + str(game.ID) + ' ended after ' + str(game.current_time) + ' minutes.')

    def sort_waiting_room(self):
        self.waiting_room.sort(key=lambda player: player.current_wait_time, reverse=True)

    def print_status(self):
        print('Queue has been running for ' + str(self.time) + ' minutes')
        print('Successfully placed ' + str(self.successes * 6) + ' players.')
        print('Failed to place ' + str(len(self.waiting_room)) + ' players.')
        average_wait_time = average([player.current_wait_time 
                                     for player in self.waiting_room])
        print('Average current wait time: ' + str(average_wait_time) + ' minutes')
        #input('Continue?') #Activate to advance time manually

    def advance_queue(self):
        self.time += 1
        self.run_games()
        for player in self.waiting_room:
            player.current_wait_time += 1
        self.sort_waiting_room()
        candidates = self.waiting_room
        selection = candidates[0] #First player we will try to find a match for

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
            if player.match_role == 'TANK':
                try:
                    dps_list.remove(player)
                    print('Removed duplicate player from DPS list')
                    input('Continue?')
                except Exception:
                    pass
                try:
                    support_list.remove(player)
                    print('Removed duplicate player from Support list')
                    input('Continue?')
                except Exception:
                    pass
            if player.match_role == 'DPS':
                try:
                    tank_list.remove(player)
                    print('Removed duplicate player from Tank list')
                    input('Continue?')
                except Exception:
                    pass
                try:
                    support_list.remove(player)
                    print('Removed duplicate player from Support list')
                    input('Continue?')
                except Exception:
                    pass
            if player.match_role == 'SUPPORT':
                try:
                    tank_list.remove(player)
                    print('Removed duplicate player from Tank list')
                    input('Continue?')
                except Exception:
                    pass
                try:
                    dps_list.remove(player)
                    print('Removed duplicate player from DPS list')
                    input('Continue?')
                except Exception:
                    pass
            return dps_list[0:2] + tank_list[0:2] + support_list[0:2]

        def process_queue(index, SR_range): #TO DO: Establish stop condition
            if index > len(candidates) - 6:
                return -1
            selection = candidates[index]
            player_list = find_match(selection, SR_range)
            if player_list:
                self.open_game(player_list)
                selection = candidates[0]
                self.successes += 1
            else:
                self.failures += 1
                index += 1
            return index
        index = 0
        while index != -1:
            index = process_queue(index, self.SR_range)
        self.print_status()
        self.successes = 0
        self.failures = 0






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


