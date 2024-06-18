import random
import math

duration_of_job = []
deadline_of_job = []

max_fitness = 0
max_fitness_bee = 0


def initial_input():
    global number_of_food_source
    global number_of_jobs
    global working_matrix
    global neighbour_search
    global counter_of_food_source

    print("Now we begin with Artificial Bee Colony")

    number_of_food_source = int(input("Enter the number of food sources:"))

    working_matrix = [0 for x in range(number_of_food_source)]

    neighbour_search = [0 for x in range(number_of_food_source)]

    counter_of_food_source = [0 for x in range(number_of_food_source)]

    print("And now we have everything we need from you. Thank You Very Much")


def read_file():
    global duration_of_job
    global deadline_of_job
    global working_list
    global number_of_jobs
    even_count = 0

    with open("saving_integers.txt") as file:
        for line in file:
            working_list = list(map(int, line.split()))
            if len(working_list) != 2:
                raise ValueError("Each line in the input file must contain exactly two integers.")
            duration_of_job.append(working_list[0])
            deadline_of_job.append(working_list[1])

    number_of_jobs = len(duration_of_job)
    print(f"Read {number_of_jobs} jobs from file.")
    if number_of_jobs < 2:
        raise ValueError("The number of jobs should be at least 2.")


def initialization():
    """Random initialization of food source"""
    for i in range(number_of_food_source):
        working_matrix[i] = random.sample(range(1, number_of_jobs + 1), number_of_jobs)

    print("The Initialized Working Matrix is:\n", working_matrix)

    for i in range(number_of_food_source):
        neighbour_search[i] = [0 for x in range(number_of_jobs)]

    for i in range(number_of_food_source):
        for j in range(number_of_jobs):
            neighbour_search[i][j] = working_matrix[i][j]

    print("Initialization Complete")

    print("\nNeighbour Search:\n", neighbour_search)
    print("\nWorking Matrix:\n", working_matrix)


def employed_bee_first():
    global max_fitness
    global max_fitness_bee
    for i in range(number_of_food_source):

        r = random.uniform(0.0, 1.0)

        if r < (1 / 3):
            """print("Swap chosen")"""
            swap(i)
        elif r < (2 / 3):
            """print("Insertion chosen")"""
            insertion(i)
        else:
            """print("Reversion chosen")"""
            reversion(i)

        if fitness_value(neighbour_search[i]) > fitness_value(working_matrix[i]):
            for j in range(number_of_jobs):
                working_matrix[i][j] = neighbour_search[i][j]

    for i in range(number_of_food_source):
        temp_fitness_value = fitness_value(working_matrix[i])
        if temp_fitness_value > max_fitness:
            max_fitness_bee = i
            max_fitness = temp_fitness_value


def employed_bee():
    global max_fitness
    global max_fitness_bee
    for i in range(number_of_food_source):

        r = random.uniform(0.0, 1.0)

        if r < (1 / 3):
            swap(i)
        elif r < (2 / 3):
            insertion(i)
        else:
            reversion(i)

        if fitness_value(neighbour_search[i]) > fitness_value(working_matrix[i]):
            for j in range(number_of_jobs):
                working_matrix[i][j] = neighbour_search[i][j]

    for i in range(number_of_food_source):
        temp_fitness_value = fitness_value(working_matrix[i])
        if temp_fitness_value > max_fitness:
            max_fitness_bee = i
            max_fitness = temp_fitness_value

    for i in range(number_of_food_source):
        if i != max_fitness_bee:
            scout_bee(i)


def scout_bee(i):
    working_matrix[i] = random.sample(range(1, number_of_jobs + 1), number_of_jobs)


def fitness_value(given=[]):
    delay = []
    total_time_taken = 0
    delay_made = 0
    for x in range(number_of_jobs):
        total_time_taken += duration_of_job[given[x] - 1]
        delay_made = total_time_taken - deadline_of_job[given[x] - 1]
        if delay_made < 0:
            delay_made = 0
        delay.append(delay_made)

    return 1 + (1 / sum(delay))


def fitness_value_normal(given=[]):
    delay = []
    total_time_taken = 0
    delay_made = 0
    for x in range(number_of_jobs):
        total_time_taken += duration_of_job[given[x] - 1]
        delay_made = total_time_taken - deadline_of_job[given[x] - 1]
        if delay_made < 0:
            delay_made = 0
        delay.append(delay_made)

    return sum(delay)


def select_two_random_numbers():
    if number_of_jobs < 2:
        raise ValueError("The number of jobs should be at least 2 for swapping, insertion, or reversion operations.")
    return random.sample(range(0, number_of_jobs), 2)


def swap(i):
    j = select_two_random_numbers()

    temp = neighbour_search[i][j[0]]
    neighbour_search[i][j[0]] = neighbour_search[i][j[1]]
    neighbour_search[i][j[1]] = temp


def insertion(i):
    j = select_two_random_numbers()

    maximum = max(j[0], j[1])
    minimum = min(j[0], j[1])

    temp = neighbour_search[i][minimum]

    forward_count = minimum

    for x in range((maximum - minimum) - 1):
        if forward_count < maximum:
            temp2 = neighbour_search[i][forward_count]
            neighbour_search[i][forward_count] = neighbour_search[i][forward_count + 1]
            neighbour_search[i][forward_count + 1] = temp2
            forward_count += 1
        else:
            neighbour_search[i][forward_count] = temp


def reversion(i):
    j = select_two_random_numbers()

    maximum = max(j[0], j[1])
    minimum = min(j[0], j[1])

    count = maximum - minimum
    forward = maximum
    backward = minimum

    for x in range(round(count / 2)):
        temp = neighbour_search[i][backward]
        neighbour_search[i][backward] = neighbour_search[i][forward]
        neighbour_search[i][forward] = temp
        backward += 1
        forward -= 1


def print_answer():
    global max_fitness
    global max_fitness_bee
    for i in range(number_of_food_source):
        temp_fitness_value = fitness_value(working_matrix[i])
        if temp_fitness_value > max_fitness:
            max_fitness_bee = i
            max_fitness = temp_fitness_value

    print("The shortest delay is for the following sequence:" + str(
        working_matrix[max_fitness_bee]) + " with the fitness value of:" +
          str(max_fitness) + " and with the normal fitness value of:" + str(
        fitness_value_normal(working_matrix[max_fitness_bee])))


def working():
    iterations = 5
    read_file()
    initial_input()
    initialization()
    employed_bee_first()
    for x in range(iterations):
        employed_bee()
        for k in range(iterations):
            employed_bee_first()
    print("\n\nThe Final Working Matrix is:\n", working_matrix)
    print_answer()


working()
