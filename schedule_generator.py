import random
from tkinter import *
from tkinter import ttk

from chore_type import chore_type
from population_initializer import *
from Interval import *
import tkinter as tk


def is_valid_schedule(chromosome, housemate_ids_original_availability_dict):
    housemate_id_solution_duration_dict = {}
    housemate_ids_availability_duration_dict = {}
    for housemate_id in housemate_ids_original_availability_dict:
        housemate_ids_availability_duration_dict[housemate_id] = housemate_ids_original_availability_dict[housemate_id].end - housemate_ids_original_availability_dict[housemate_id].start

    for gene in chromosome.values():
        housemate_id = gene.housemate_id
        duration = gene.duration
        if housemate_id not in housemate_id_solution_duration_dict:
            housemate_id_solution_duration_dict[housemate_id] = 0
        housemate_id_solution_duration_dict[housemate_id] += duration

    for housemate_id, total_duration in housemate_id_solution_duration_dict.items():
        original_availability = housemate_ids_availability_duration_dict.get(housemate_id)
        if original_availability is None or total_duration > original_availability:
            return False

    return True


def fittest_parents(pop, total_duration, housemate_count, housemate_ids_availability_dict):
    min_fitness1 = float('inf')  # Initialize minimum fitness values
    min_fitness2 = float('inf')
    min_chromosome1 = None  # Initialize chromosomes with minimum fitness values
    min_chromosome2 = None

    for chromosome in pop:
        if is_valid_schedule(chromosome, housemate_ids_availability_dict):
            if all_housemates_chosen(chromosome, housemate_count):
                housemate_load_dict = {}
                housemate_ratio_to_total_chores_duration = []
                housemate_ratio_distance = []

                for chore, gene in chromosome.items():
                    housemate_load_dict[gene.housemate_id] = housemate_load_dict.get(gene.housemate_id, 0) + gene.duration

                for housemate_load in housemate_load_dict.values():
                    housemate_ratio_to_total_chores_duration.append(housemate_load / total_duration)

                for ratio in housemate_ratio_to_total_chores_duration:
                    housemate_ratio_distance.append(abs(ratio - (1 / housemate_count)))

                fitness = sum(housemate_ratio_distance)

                if fitness < min_fitness1:
                    min_fitness2 = min_fitness1
                    min_chromosome2 = min_chromosome1
                    min_fitness1 = fitness
                    min_chromosome1 = chromosome
                elif fitness < min_fitness2:
                    min_fitness2 = fitness
                    min_chromosome2 = chromosome

    return min_chromosome1, min_chromosome2


def all_housemates_chosen(chromosome, housemate_count):
    housemates = set()
    for chore, gene in chromosome.items():
        housemates.add(gene.housemate_id)
    return len(housemates) == housemate_count


def swap(first_gene, second_gene):
    pass

def chromosome_to_dict(chromosome):
    gene_info_dict = {}

    for gene in chromosome:
        chore_type = gene.chore_type
        gene_info = {'duration': gene.duration, 'start_time': gene.start_time, 'housemate_id': gene.housemate_id}

        if chore_type not in gene_info_dict:
            gene_info_dict[chore_type] = []

        gene_info_dict[chore_type].append(gene_info)

    return gene_info_dict

def crossover(first_parent, second_parent, chore_type_list):
    if (first_parent is not None) and (second_parent is not None):
        chore = random.choice(chore_type_list)
        temp = first_parent[chore]
        first_parent[chore] = second_parent[chore]
        second_parent[chore] = temp


def generate_schedule_using_ga(root, chore_duration_dict, housemate_ids_availability_dict):
    evolution_pop = []
    pop_size = 100
    N = 10

    init_pop = initialize_population(pop_size, chore_duration_dict, housemate_ids_availability_dict)

    first_parent, second_parent = fittest_parents(init_pop, sum(chore_duration_dict.values()), len(housemate_ids_availability_dict), housemate_ids_availability_dict)

    crossover(first_parent, second_parent, list(chore_duration_dict.keys()))

    evolution_pop.append(first_parent)
    evolution_pop.append(second_parent)

    for i in range(N):
        crossover(first_parent, second_parent, list(chore_duration_dict.keys()))
        evolution_pop.append(first_parent)
        evolution_pop.append(second_parent)
        first_parent, second_parent = fittest_parents(init_pop, sum(chore_duration_dict.values()),
                                                      len(housemate_ids_availability_dict), housemate_ids_availability_dict)

    elite_parents = []
    elite_parents.append(first_parent)
    elite_parents.append(second_parent)
    create_tree_view(root, elite_parents)

def create_tree_view(root, elite_parents):
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    for i, chromosome in enumerate(elite_parents):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=f'Schedule {i + 1}')
        frame_tab = ttk.Frame(tab)
        frame_tab.pack(padx=0, pady=0)

        tree = ttk.Treeview(frame_tab)
        tree["columns"] = ("Chore Type", "Start Time", "Duration", "Housemate ID")

        # Define columns
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Chore Type", anchor=tk.W, width=70)
        tree.column("Start Time", anchor=tk.CENTER, width=100)
        tree.column("Duration", anchor=tk.CENTER, width=100)
        tree.column("Housemate ID", anchor=tk.CENTER, width=100)

        # Define column headings
        tree.heading("Chore Type", text="Chore Type")
        tree.heading("Start Time", text="Start Time")
        tree.heading("Duration", text="Duration")
        tree.heading("Housemate ID", text="Housemate ID")

        if (chromosome is not None):
            for chore, gene in chromosome.items():
                start_time = gene.start_time
                duration = gene.duration
                am_pm = "AM" if start_time < 12 else "PM"
                hour_hours = "hour" if duration < 2 else "hours"
                start_time = str(start_time) + " " + am_pm
                duration = str(duration) + " " + hour_hours
                housemate_id = gene.housemate_id
                tree.insert("", tk.END, values=(chore.name, start_time, duration, housemate_id))

            tree.pack()
