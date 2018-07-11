from classes import Farm

play = True

def get_input_continue(farm):
    prompt_str = "Current map:\n" + \
                 str(farm) + "\n" * 2 + \
                "Which way would you like to go? (" + ", ".join(farm.find_possible_directions()) + "): "
    return input(prompt_str)

current_farm = Farm.FarmMap()
    
while play:    
    user_in = get_input_continue(current_farm)
    try:
        current_farm.move(user_in)
        print('')
    except ValueError as err:
        print(err.args[0])
        print('')
    except OverflowError as err:
        print(err.args[0])
        play = False
