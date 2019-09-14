from Game import Game
from utilities import average, mode

class Queue():
    waiting_room = [] #contains multiple copies of players queuing for multiple roles
    active_games = []
    next_game_ID = 0
    successes = 0
    failures = 0
    time = 0
    base_SR_range = 200 #Base max range of SRs allowed to form a game
    range_boost = 10

    def get_SR_range(self, player):
        return self.base_SR_range + player.current_wait_time * self.range_boost

    def open_game(self, player_list):
        game = Game(player_list, self.next_game_ID)
        self.next_game_ID += 1
        for player in player_list:
            self.waiting_room.remove(player)
            player.current_wait_time = 0
        self.active_games.append(game)
        #print(game)
        
    def run_games(self):
        for game in self.active_games:
            game.current_time += 1
            if game.current_time == game.end_time:
                self.close_game(game)

    def close_game(self, game):
        self.active_games.remove(game)
        testing = True
        for player in game.player_list:
            if testing == True:
                self.waiting_room.append(player)
                continue
            if player.leave_queue():
                pass
            else:
                print('Player ' + str(player.ID) + ' returned to queue')
                self.waiting_room.append(player)
        #print('Game ' + str(game.ID) + ' ended after ' + str(game.current_time) + ' minutes.')

    def sort_waiting_room(self):
        self.waiting_room.sort(key=lambda player: player.current_wait_time, reverse=True)

    def print_status(self):
        print('Queue has been running for ' + str(self.time) + ' minutes')
        print('Successfully placed ' + str(self.successes * 12) + ' players.')
        print('Failed to place ' + str(len(self.waiting_room)) + ' players.')
        print('Skipped ' + str(len([player for player in self.waiting_room
                                                 if player.tested == False])) + ' players')
        wait_times = [player.current_wait_time for player in self.waiting_room]
        average_wait_time = average(wait_times)
        print('Average current wait time: ' + str(average_wait_time) + ' minutes')
        median_wait_time = wait_times[int(len(wait_times)/2)]
        print('Median current wait time: ' + str(median_wait_time) + ' minutes')
        modal_wait_time = mode(wait_times)
        print('Modal current wait time: ' + str(modal_wait_time) + ' minutes')
        print('Max current wait time: ' + str(max(wait_times)) + ' minutes')
        game_SR_ranges = [game.SR_range for game in self.active_games]
        average_SR_range = average(game_SR_ranges)
        print('Average active game SR range: ' + str(average_SR_range) + ' SR')
        median_SR_range = game_SR_ranges[int(len(game_SR_ranges)/2)]
        print('Median active game SR range: ' + str(median_SR_range) + ' SR')
        max_SR_range = max(game_SR_ranges)
        print('Max active game SR range: ' + str(max_SR_range) + ' SR')
        
              
        #input('Continue?') #Activate to advance time manually

    def advance_queue(self):
        self.time += 1
        self.run_games()
        for player in self.waiting_room:
            player.current_wait_time += 1
            player.tested = False
        self.sort_waiting_room()
        candidates = self.waiting_room
        selection = candidates[0] #First player we will try to find a match for

        def tank_candidates():
            return [player for player in candidates if player.match_role == 'TANK']

        def dps_candidates():
            return [player for player in candidates if player.match_role == 'DPS']

        def support_candidates():
            return [player for player in candidates if player.match_role == 'SUPPORT']

        def find_match(player): #Returns player list or False if no valid SR matches
            SR_range = self.get_SR_range(player)
            if SR_range > 500:
                print(SR_range)
            SR_range = range(int(player.match_SR() - SR_range / 2),
                             int(player.match_SR() + SR_range / 2))
            dps_list = [player for player in dps_candidates()
                        if player.dps_SR in SR_range]
            tank_list = [player for player in tank_candidates()
                         if player.tank_SR in SR_range]
            support_list = [player for player in support_candidates()
                            if player.support_SR in SR_range]
            if len(dps_list) < 4 or len(tank_list) < 4 or len(support_list) < 4:
                return False
            dps_IDs = [player.ID for player in dps_list]
            tank_IDs = [player.ID for player in tank_list]
            support_IDs = [player.ID for player in support_list]
            for ID in dps_IDs:
                if ID in tank_IDs or ID in support_IDs:
                    print('Duplicate ID: ' + str(ID))
                    input('Continue?')
            for ID in tank_IDs:
                if ID in support_IDs:
                    print('Duplicate ID: ' + str(ID))
                    input('Continue?')
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
            return dps_list[0:4] + tank_list[0:4] + support_list[0:4]

        def find_match_quick(player): #TO DO - check for duplicate IDs
            SR_range = self.get_SR_range(player)
            if SR_range > 500:
                print(SR_range)
            SR_range = range(int(player.match_SR() - SR_range / 2),
                             int(player.match_SR() + SR_range / 2))
            dps_list = []
            for player in dps_candidates():
                if player.dps_SR in SR_range:
                    dps_list.append(player)
                    if len(dps_list) == 4:
                        break
            tank_list = []
            for player in tank_candidates():
                if player.tank_SR in SR_range:
                    tank_list.append(player)
                    if len(tank_list) == 4:
                        break
            support_list = []
            for player in support_candidates():
                if player.support_SR in SR_range:
                    support_list.append(player)
                    if len(support_list) == 4:
                        break
            if len(dps_list) < 4 or len(tank_list) < 4 or len(support_list) < 4:
                return False
            return dps_list + tank_list + support_list

        def process_queue(index):
            if index > len(candidates) - 12:
                return -1
            selection = candidates[index]
            selection.tested = True
            player_list = find_match_quick(selection)
            if player_list:
                self.open_game(player_list)
                selection = candidates[0]
                self.successes += 1
            else:
                self.failures += 1
                index += 1
            return index
        index = 0
        count = 1
        print('Players in waiting room: ' + str(len(self.waiting_room)))
        while index != -1:
            if count % 100 == 0:
                print('Processing player ' + str(count))
            count += 1
            index = process_queue(index)
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


