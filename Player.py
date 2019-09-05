from utilities import roll, SR_generator, off_role_SR

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

    def __init__(self):
        Player.generate_role(self)
        Player.generate_SR(self)

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
        return '\n'.join([player_string, role_string, tank_SR_string,
                         dps_SR_string, support_SR_string])
