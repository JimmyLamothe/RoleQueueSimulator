
from utilities import roll, SR_generator, off_role_SR, time_limit_generator
from utilities import min_session_generator, max_session_generator

class Player:
    # Which roles player will queue for
    tank = False
    dps = False
    support = False
    # SR per role
    tank_SR = 0
    dps_SR = 0
    support_SR = 0
    # Max SR
    SR = 0
    # Player ID - Assigned by Populator
    ID = None
    # Wait times per role
    tank_times = []
    dps_times = []
    support_times = []
    # Queue style
    min_session_time = 0
    max_session_time = 0
    # Chance to stop after game according to current session time
    min_stop_chance = 0.05
    med_stop_chance = 0.10
    max_stop_chance = 0.90
    # When wait times are longer than queue_time_limit, player more likely to quit
    queue_time_limit = 0
    chance_increase = 0.15
    # Wait times for current session
    session_wait_times = []
    # Time in active session
    active_session_time = 0
    # Time in wait queue
    current_wait_time = 0
    # Roles currently queueing for
    active_roles = []
    # Role currently matching for
    match_role = None

    def generate_role(self):
        #chance player will queue for each role
        support_chance = 0.25
        tank_chance = 0.15
        dps_chance = 0.9
        if roll(support_chance):
            self.support = True
        if roll(tank_chance):
            self.tank = True
        if roll(dps_chance):
            self.dps = True
        if not self.tank and not self.support and not self.dps:
            Player.generate_role(self)

    def generate_queue_style(self):
        self.min_session_time = min_session_generator()
        self.max_session_time = max_session_generator()
        self.queue_time_limit = time_limit_generator()

    def leave_queue(self):
        chance = 1
        session_time = self.active_session_time
        if session_time < self.min_session_time:
            chance = self.min_stop_chance
        elif session_time < self.max_session_time:
            chance = self.med_stop_chance
        else:
            chance = self.max_stop_chance
        if self.current_wait_time > self.queue_time_limit:
            chance += self.chance_increase
        if roll(chance):
            return True
        return False

    def generate_SR(self):
        base_SR = SR_generator()
        if self.tank:
            self.tank_SR = base_SR
            self.SR = base_SR
        else:
            self.tank_SR = off_role_SR(base_SR)
        if self.dps:
            self.dps_SR = base_SR
            self.SR = base_SR
        else:
            self.dps_SR = off_role_SR(base_SR)
        if self.support:
            self.support_SR = base_SR
            self.SR = base_SR
        else:
            self.support_SR = off_role_SR(base_SR)

    def match_SR(self):
        if self.match_role == 'TANK':
            return self.tank_SR
        if self.match_role == 'DPS':
            return self.dps_SR
        if self.match_role == 'SUPPORT':
            return self.support_SR
        else:
            print('Player.match_SR method failed, using max SR')
            return self.SR #Shouldn't happen!

    def __init__(self):
        Player.generate_role(self)
        Player.generate_SR(self)
        Player.generate_queue_style(self)

    def __repr__(self):
        player_string = 'Player:'
        if self.ID:
            player_string += ' ' + str(self.ID)
        roles = []
        if self.tank:
            roles.append('TANK')
        if self.dps:
            roles.append('DPS')
        if self.support:
            roles.append('SUPPORT')
        role_string = ', '.join(roles)
        tank_SR_string = 'TANK_SR: ' + str(self.tank_SR)
        dps_SR_string = 'DPS_SR: ' + str(self.dps_SR)
        support_SR_string = 'SUPPORT_SR: ' + str(self.support_SR)
        min_session_time_string = 'Minimum session time: ' + str(self.min_session_time)
        max_session_time_string = 'Maximum session time: ' + str(self.max_session_time)
        queue_time_limit_string = 'Maximum wait time: ' + str(self.queue_time_limit)
        current_wait_time_string = 'Current wait time: ' + str(self.current_wait_time)
        match_role_string = 'Current role: ' + str(self.match_role)
        return '\n'.join([player_string, role_string, tank_SR_string,
                         dps_SR_string, support_SR_string, min_session_time_string,
                          max_session_time_string, queue_time_limit_string,
                          current_wait_time_string, match_role_string, '\n'])
