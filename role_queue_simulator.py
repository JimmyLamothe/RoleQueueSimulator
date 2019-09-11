import Population, Queue

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
    test_queue = Queue.Queue()
    test_queue.waiting_room = test_population.player_list
    while(test_queue.time < 300):
        print('Current time: ' + str(test_queue.time))
        #input('Continue?')
        test_queue.advance_queue()
    

test_queue()
