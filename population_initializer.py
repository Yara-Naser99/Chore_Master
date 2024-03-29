import copy
import random
from Gene import *
from Interval import *
from Chromosome import Chromosome

def initialize_population(pop_size, chore_duration_dict, housemate_ids_availability_dict):
    init_pop = []

    for i in range(pop_size):
        chromosome = {}
        housemate_ids_availability_dict_local_copy = copy.deepcopy(housemate_ids_availability_dict)
        housemate_ids_chosen = []

        for chore, duration in chore_duration_dict.items():
            available_housemate_ids = choose_start_time_based_on_available_housemate(housemate_ids_availability_dict_local_copy, duration)

            if len(housemate_ids_chosen) >= len(housemate_ids_availability_dict_local_copy):
                housemate_id = fairly_choose_housemate(available_housemate_ids, housemate_ids_chosen)
            else:
                housemate_id = random.choice(available_housemate_ids)

            start_time = housemate_ids_availability_dict_local_copy[housemate_id].start

            chromosome[chore] = Gene(duration, start_time, housemate_id)
            housemate_ids_chosen.append(housemate_id)
            update_housemate_availability(housemate_id, duration, housemate_ids_availability_dict_local_copy)


        init_pop.append(chromosome)

    return init_pop

def choose_start_time_based_on_available_housemate(housemate_ids_availability_dict, chore_duration):
    available_housemate_ids = []
    for housemate_id, interval in housemate_ids_availability_dict.items():
        if isinstance(interval, Interval):
            start, end = interval.start, interval.end
            if end - start >= chore_duration:
                available_housemate_ids.append(housemate_id)
    return available_housemate_ids

def update_housemate_availability(housemate_id, chore_duration, housemate_ids_availability_dict):
    new_availability_start = (housemate_ids_availability_dict[housemate_id]).start + chore_duration
    availability_end = (housemate_ids_availability_dict[housemate_id]).end
    housemate_ids_availability_dict[housemate_id] = Interval(new_availability_start, (housemate_ids_availability_dict[housemate_id]).end)

def fairly_choose_housemate(housemate_ids, housemate_ids_chosen):
    housemate_ids_chosen_dict = {}
    for housemate_id in housemate_ids_chosen:
        housemate_ids_chosen_dict[housemate_id] = housemate_ids_chosen_dict.get(housemate_id, 0) + 1
    min_housemate_id = min(housemate_ids_chosen_dict, key=housemate_ids_chosen_dict.get)
    return min_housemate_id