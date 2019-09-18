import random, sys, config

def roll(chance):
    result = random.random()
    if result < chance:
        return True
    return False

def average(lst):
    return int(sum(lst) / len(lst))

def median(lst):
    return lst[int(len(lst) / 2)]

def mode(lst):
    return max(set(lst), key = lst.count)

def SR_generator():
    base = 2200
    modifier = random.gauss(0, 700)
    if modifier < 0:
        modifier = int(modifier * 0.7)
    else:
        modifier = int(modifier)
    SR = base + modifier
    return SR

def SR_tester(iterations):
    min = 2200
    max = 2200
    for i in range(iterations):
        SR = SR_generator()
        if SR > max:
            max = SR
        elif SR < min:
            min = SR
    print('maximum SR: ' + str(max), 'minimum SR: ' + str(min))

def off_role_SR(base_SR):
    modifier = int(abs(random.gauss(0, 300)))
    return base_SR - modifier

def rank(SR):
    if SR < 1500:
        return 'BRONZE'
    if SR < 2000:
        return 'SILVER'
    if SR < 2500:
        return 'GOLD'
    if SR < 3000:
        return 'PLATINUM'
    if SR < 3500:
        return 'DIAMOND'
    if SR < 4000:
        return 'MASTER'
    else:
        return 'GM'

def role(player):
    if player.tank and player.dps and player.support:
        return 'FLEX'
    if player.tank and player.dps:
        return 'TANK - DPS'
    if player.tank and player.support:
        return 'TANK - SUPPORT'
    if player.dps and player.support:
        return 'DPS - SUPPORT'
    if player.tank:
        return 'TANK'
    if player.dps:
        return 'DPS'
    if player.support:
        return 'SUPPORT'
    else:
        print('Invalid role assignment, bug check')
        raise Exception

def game_time():
    return random.randint(7,18)

def min_session_generator():
    return random.randint(20, 60)

def max_session_generator():
    return random.randint(90, 360)

def time_limit_generator():
    return random.randint(5, 20)    

def test_print(*args, **kwargs):
    if config.skip_print:
        pass
    else:
        print(*args, **kwargs)
