from utilities import game_time

class Game():
    ID = None
    current_time = 0
    end_time = 0
    SR_range = 0
    player_list = []

    def __init__(self, player_list, ID):
        self.player_list = player_list
        self.ID = ID
        self.end_time = game_time()
        SR_list = [player.match_SR() for player in player_list]
        self.SR_range = max(SR_list) - min(SR_list)

    def __repr__(self):
        player_string = ''
        for number, player in enumerate(self.player_list):
            player_string += 'PLAYER ' + str(number + 1) + ': ' + str(player.ID) + '\n'
        current_time_string = 'Current time: ' + str(self.current_time)
        end_time_string = 'End time: ' + str(self.end_time)
        return '\n'.join([player_string, current_time_string, end_time_string])

        
