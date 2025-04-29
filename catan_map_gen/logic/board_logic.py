import random

def generate_resources(player_count):
    if player_count == 4:
        resources = (
            ['Wood'] * 4 +
            ['Sheep'] * 4 +
            ['Wheat'] * 4 +
            ['Brick'] * 3 +
            ['Ore'] * 3 +
            ['Desert'] * 1
        )
        layout = [3, 4, 5, 4, 3]
        numbers = [2, 3, 3, 4, 4, 5, 5, 6, 6,
                   8, 8, 9, 9, 10, 10, 11, 11, 12]
        ports = ['3:1'] * 4 + ['Wood', 'Brick', 'Ore', 'Wheat', 'Sheep']
        port_slots = ['port'] * 9
    elif player_count == 6:
        resources = (
            ['Wood'] * 6 +
            ['Sheep'] * 6 +
            ['Wheat'] * 6 +
            ['Brick'] * 5 +
            ['Ore'] * 5 +
            ['Desert'] * 2
        )
        layout = [3, 4, 5, 6, 5, 4, 3]
        numbers = [2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12] 
        ports = ['3:1'] * 6 + ['Wood', 'Brick', 'Ore', 'Wheat', 'Sheep']
        port_slots = ['port'] * 11
    else:
        return None, None, None, None, None

    return resources, layout, numbers, ports, port_slots

def build_board(resources, numbers):
    resource_with_numbers = []
    number_index = 0
    for res in resources:
        if res == 'Desert':
            resource_with_numbers.append((res, None))
        else:
            if number_index < len(numbers):
                resource_with_numbers.append((res, numbers[number_index]))
                number_index += 1
            else:
                resource_with_numbers.append((res, None))  # No number for extra tiles
    return resource_with_numbers
