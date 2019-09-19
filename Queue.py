from Game import Game
from utilities import average, median, mode, test_print, time_function

class Queue():
    waiting_room = []
    active_games = []
    next_game_ID = 0
    successes = 0
    failures = 0
    time = 0
    base_SR_range = 200 #Base max range of SRs allowed to form a game
    range_boost = 10

    def get_roles(self):
        for player in self.waiting_room:
            player.get_active_roles()

    def get_SR_range(self, player):
        return self.base_SR_range + player.current_wait_time * self.range_boost

    def open_game(self, player_list):
        game = Game(player_list, self.next_game_ID)
        self.next_game_ID += 1
        for player in player_list:
            self.waiting_room.remove(player)
            player.current_wait_time = 0
        self.active_games.append(game)
        #test_print(game)
        
    def run_games(self):
        for game in self.active_games:
            game.current_time += 1
            if game.current_time == game.end_time:
                self.close_game(game)

    def close_game(self, game):
        self.active_games.remove(game)
        testing = True
        for player in game.player_list:
            if testing == True: #Players entering and leaving queue not implemented
                self.waiting_room.append(player)
                continue
            if player.leave_queue():
                pass
            else:
                test_print('Player ' + str(player.ID) + ' returned to queue')
                self.waiting_room.append(player)
        #test_print('Game ' + str(game.ID) + ' ended after ' + str(game.current_time) + ' minutes.')

    def sort_waiting_room(self):
        self.waiting_room.sort(key=lambda player: player.current_wait_time, reverse=True)

    def print_status(self):
        print('Queue has been running for ' + str(self.time) + ' minutes')
        print('Successfully placed ' + str(self.successes * 12) + ' players.')
        print('Failed to place ' + str(len(self.waiting_room)) + ' players.')
        print('Skipped ' + str(len([player for player in self.waiting_room
                                                 if player.tested == False])) + ' players')
        def print_wait_times(wait_times, string):
            print('Number of ' + string + ' in queue: ' + str(len(wait_times)) + ' player.')
            print('Average current ' + string + ' wait time: ' + str(average(wait_times)) + ' minutes')
            print('Median current ' + string + ' wait time: ' + str(median(wait_times)) + ' minutes')
            print('Modal current ' + string + ' wait time: ' + str(mode(wait_times)) + ' minutes')
            print('Max current ' + string + ' wait time: ' + str(max(wait_times)) + ' minutes')

        def print_ranks(player_list):
            bronze = [player for player in player_list if player.get_rank() == 'BRONZE']
            silver = [player for player in player_list if player.get_rank() == 'SILVER']
            gold = [player for player in player_list if player.get_rank() == 'GOLD']
            platinum = [player for player in player_list if player.get_rank() == 'PLATINUM']
            diamond = [player for player in player_list if player.get_rank() == 'DIAMOND']
            master = [player for player in player_list if player.get_rank() == 'MASTER']
            GM = [player for player in player_list if player.get_rank() == 'GM']
            print('Bronze: ' + str(len(bronze)))
            print('Silver: ' + str(len(silver)))
            print('Gold: ' + str(len(gold)))
            print('Platinum: ' + str(len(platinum)))
            print('Diamond: ' + str(len(diamond)))
            print('Master: ' + str(len(master)))
            print('GM: ' + str(len(GM)))
        all_wait_times = [player.current_wait_time for player in self.waiting_room]
        print_wait_times(all_wait_times, 'player')
        dps_queue = [player for player in self.waiting_room
                     if 'DPS' in player.active_roles]
        dps_wait_times = [player.current_wait_time for player in dps_queue]
        print_wait_times(dps_wait_times, 'DPS')
        print_ranks(dps_queue)
        tank_queue = [player for player in self.waiting_room
                     if 'TANK' in player.active_roles]
        tank_wait_times = [player.current_wait_time for player in tank_queue]
        print_wait_times(tank_wait_times, 'Tank')
        print_ranks(tank_queue)
        support_queue = [player for player in self.waiting_room
                     if 'SUPPORT' in player.active_roles]
        support_wait_times = [player.current_wait_time for player in support_queue]
        print_wait_times(support_wait_times, 'Support')
        print_ranks(support_queue)
        bronze_wait_times = [player.current_wait_time for player in self.waiting_room
                          if player.get_rank() == 'BRONZE']
        print_wait_times(bronze_wait_times, 'Bronze')
        silver_wait_times = [player.current_wait_time for player in self.waiting_room
                          if player.get_rank() == 'SILVER']
        print_wait_times(silver_wait_times, 'Silver')
        gold_wait_times = [player.current_wait_time for player in self.waiting_room
                          if player.get_rank() == 'GOLD']
        print_wait_times(gold_wait_times, 'Gold')
        platinum_wait_times = [player.current_wait_time for player in self.waiting_room
                          if player.get_rank() == 'PLATINUM']
        print_wait_times(platinum_wait_times, 'Platinum')
        diamond_wait_times = [player.current_wait_time for player in self.waiting_room
                          if player.get_rank() == 'DIAMOND']
        print_wait_times(diamond_wait_times, 'Diamond')
        master_wait_times = [player.current_wait_time for player in self.waiting_room
                          if player.get_rank() == 'MASTER']
        print_wait_times(master_wait_times, 'Master')
        gm_wait_times = [player.current_wait_time for player in self.waiting_room
                          if player.get_rank() == 'GM']
        print_wait_times(gm_wait_times, 'GM')
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
        tank_candidates = [player for player in self.waiting_room
                           if 'TANK' in player.active_roles]
        dps_candidates = [player for player in self.waiting_room
                          if 'DPS' in player.active_roles]
        support_candidates = [player for player in self.waiting_room
                              if 'SUPPORT' in player.active_roles]

        def remove_from_candidates(player):
            if 'TANK' in player.active_roles:
                tank_candidates.remove(player)
            if 'DPS' in player.active_roles:
                dps_candidates.remove(player)
            if 'SUPPORT' in player.active_roles:
                support_candidates.remove(player)

        def find_match(player): 
            player.get_active_roles()
            for role in player.active_roles:
                player.match_role = role
                test_print('Finding match for following player as a ' + role + ':')
                test_print(player)
                player_list = find_match_role(player)
                if player_list:
                    test_print(player_list)
                    for player in player_list:
                        remove_from_candidates(player)
                    return player_list
                else:
                    continue #Skip rest for speed, comment out to print info
                    test_print('Failed to find match for player ' + str(player.ID) + ' as a ' + role)
                    SR_range = self.get_SR_range(player)
                    min_SR = int(player.match_SR() - SR_range / 2)
                    max_SR = int(player.match_SR() + SR_range / 2)
                    valid_dps_candidates = [dps for dps in dps_candidates
                                            if dps.dps_SR > min_SR
                                            and dps.dps_SR < max_SR]
                    valid_tank_candidates = [tank for tank in tank_candidates
                                             if tank.tank_SR > min_SR
                                             and tank.tank_SR < max_SR]
                    valid_support_candidates = [support for support in support_candidates
                                             if support.support_SR > min_SR
                                             and support.support_SR < max_SR]
                    test_print('Total number of DPS in queue: ' +
                               str(len(dps_candidates)))
                    test_print('Number of DPS with valid SR: ' +
                               str(len(valid_dps_candidates)))
                    test_print('Total number of tanks in queue: ' +
                               str(len(tank_candidates)))
                    test_print('Number of tanks with valid SR: ' +
                               str(len(valid_tank_candidates)))
                    test_print('Total number of supports in queue: '
                               + str(len(support_candidates)))
                    test_print('Number of supports with valid SR: ' +
                               str(len(valid_support_candidates)))
                    continue
            test_print('Failed to find match for player ' + str(player.ID) + ' in any role')
            test_print('Active roles : ' + str(player.active_roles))
            #input('Continue?')
            return False

        def find_match_role(player): #Key function to be improved for speed
            SR_range = self.get_SR_range(player)
            if SR_range > 500:
                print(SR_range)
            SR_range = range(int(player.match_SR() - SR_range / 2),
                             int(player.match_SR() + SR_range / 2))

            player_list = []
            player_list.append(player)

            tank_list = []
            support_list = []
            dps_list = []

            if player.match_role == 'TANK':
                tank_list.append(player)
            elif player.match_role == 'SUPPORT':
                support_list.append(player)
            elif player.match_role == 'DPS':
                dps_list.append(player)
            else:
                print('Following player should have match role:')
                print(player)
                raise ValueError
            def get_lists():
                return '\n'.join(['Player List: ' + '\n'.join(str(player) for player in player_list),
                                  'Tank List: ' + '\n'.join(str(player) for player in tank_list),
                                  'Support List: ' + '\n'.join(str(player) for player in support_list),
                                  'DPS List: ' + '\n'.join(str(player) for player in dps_list)])
            test_print(get_lists())
                               
            for candidate in tank_candidates:
                #test_print(str(candidate.ID))
                #test_print('Tank: ' + str(candidate.tank))
                #test_print(candidate.tank_SR)
                #input('Testing for SR match')
                if candidate.tank_SR in SR_range and candidate not in player_list:
                    candidate.match_role = 'TANK'
                    tank_list.append(candidate)
                    player_list.append(candidate)
                    #input('Match found!')
                    if len(tank_list) == 4:
                        break

            test_print(get_lists())

            for candidate in support_candidates:
                #test_print(str(candidate.ID))
                #test_print('Support: ' + str(candidate.support))
                #test_print(candidate.support_SR)
                #input('Testing for SR match')
                if candidate.support_SR in SR_range and candidate not in player_list:
                    candidate.match_role = 'SUPPORT'
                    support_list.append(candidate)
                    player_list.append(candidate)
                    #input('Match found!')
                    if len(support_list) == 4:
                        break

            test_print(get_lists())

            for candidate in dps_candidates:
                #test_print(str(candidate.ID))
                #test_print('DPS: ' + str(candidate.dps))
                #test_print(str(candidate.dps_SR))
                #input('Testing for SR match')
                if candidate.dps_SR in SR_range and candidate not in player_list:
                    candidate.match_role = 'DPS'
                    dps_list.append(candidate)
                    player_list.append(candidate)
                    #input('Match found!')
                    if len(dps_list) == 4:
                        break

            test_print(get_lists())

            if len(player_list) < 12:
                return False
            #test_print(player_list)
            #input('Continue?')
            return player_list

        def process_queue(index):
            if index >= len(tank_candidates):
                return -1
            selection = tank_candidates[index]
            selection.tested = True
            player_list = find_match(selection)
            if player_list:
                self.open_game(player_list)
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


