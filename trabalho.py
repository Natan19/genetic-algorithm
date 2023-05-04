import random
from math import ceil 

MAX_POPULATION=10
MAX_PRODUCTIVITY=10
DEADLINE=100
MAX_JOIN_DATE=DEADLINE//2
GOAL=1500
MAX_EXPERIENCE=5
MIN_EXPERIENCE=1 
EXPERIENCE_FACTOR_MULTIPLIER=2
DATE_THRESHOLD_DEBUFF=30


def generate_initial_population(max_population):
    population = []
    for i in range(0,max_population):
        # engineer is defined by a tuple (id, productivity, date_joined, experience)
        population.append((i, random.randrange(0, MAX_PRODUCTIVITY), random.randrange(0, MAX_JOIN_DATE), random.randrange(MIN_EXPERIENCE, MAX_EXPERIENCE)))
    return population

def calculate_fitness(population):
    individual_fitness_list = []
    total_fitness=0
    for i in range (0, len(population)):
        engineer=population[i]
        # fitness is defined by multiplying the daily fitness factor by the number of days of work left from date joined to deadline
        fitness=((engineer[1]/DEADLINE)*(DEADLINE-engineer[2]))
        fitness=fitness*(1-((engineer[3]*2)/100))
        individual_fitness_list.append((engineer[0], fitness))
        if engineer[2] >= DATE_THRESHOLD_DEBUFF:
            total_fitness+=fitness//2
        else:
            total_fitness+=fitness
    return individual_fitness_list, ceil(total_fitness) 

def selection(population):
    random_ids_list=[random.randint(0, len(population)) for _ in range(0,len(population))]
    selected_individuals=[]
    for i in random_ids_list:
        accessor=i-1
        selected_individuals.append(population[accessor])
    return selected_individuals 

def crossover(selected_individuals):
    number_of_pairs=len(selected_individuals)//2
    new_individuals=[]
    for i in range(0,number_of_pairs):
        first_engineer=selected_individuals[i]
        second_engineer=selected_individuals[i+1]
        new_individuals.append(mutate((i, (first_engineer[1]/2)+second_engineer[1], second_engineer[2], ceil(first_engineer[3]*0.1))))
        new_individuals.append(mutate((i+1, (second_engineer[1]/2)+first_engineer[1], first_engineer[2], ceil(second_engineer[3]*0.1)))) 

    return new_individuals

def mutate(individual):
    random_generation_effect=random_signed_integer(0,15)
    return (individual[0], individual[1]+(random_generation_effect), individual[2], individual[3])

def random_signed_integer(min_value, max_value):
    number = random.randint(min_value, max_value)
    sign = random.choice([-1, 1])
    return number * sign 


def run(generation, count):
    if len(generation)==0:
        population=generate_initial_population(MAX_POPULATION)
        print("Initial population:", population)
        indiv,total=calculate_fitness(population)
        print("Initial population fitness", total)
        return run(population, count)

    select_pop=selection(generation)
    print("Individuals selected", select_pop)
    new_generation=crossover(select_pop)
    print("New generation", new_generation)
    new_gen_indiv,new_gen_total=calculate_fitness(new_generation)
    print("New generation fitness", new_gen_total)
    
    if count == 10:
        return
    elif new_gen_total>=GOAL:
        return
    return run(new_generation, count+1)
        
run([], 0)
