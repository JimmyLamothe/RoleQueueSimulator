import sys
import Population, Queue, config

players = 10000

for arg in sys.argv:
    if arg == 'skip_print':
        config.skip_print = True
    try:
        players = int(arg)
    except Exception:
        pass

def test_queue():
    from Population import Population
    import random
    test_population = Population(players)
    for player in test_population.player_list:
        player.current_wait_time = 0
    test_queue = Queue.Queue()
    test_queue.waiting_room = test_population.player_list
    test_queue.get_roles()
    while(test_queue.time < 300):
        print('Current time: ' + str(test_queue.time))
        #input('Continue?')
        test_queue.advance_queue()
    

test_queue()
