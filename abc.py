import random
import math

class ArtificialBeeColony:
    def __init__(self, num_jobs, job_durations, job_deadlines, num_food_sources, max_iterations):
        self.num_jobs = num_jobs
        self.job_durations = job_durations
        self.job_deadlines = job_deadlines
        self.num_food_sources = num_food_sources
        self.max_iterations = max_iterations
        
        self.working_matrix = []
        self.neighbour_search = []
        self.counter_of_food_source = []
        self.best_solution = []
        self.max_fitness = -1
        self.max_fitness_bee = 0
        self.q_table = {}

    def initialize(self):
        for i in range(self.num_food_sources):
            solution = random.sample(range(1, self.num_jobs + 1), self.num_jobs)
            self.working_matrix.append(solution)
            self.neighbour_search.append(solution[:])
            self.q_table[tuple(solution)] = 0
        
        self.update_best_solution()

    def fitness_value(self, solution):
        delay = []
        total_time_taken = 0
        delay_made = 0
        for job in solution:
            total_time_taken += self.job_durations[job - 1]
            delay_made = total_time_taken - self.job_deadlines[job - 1]
            if delay_made < 0:
                delay_made = 0
            delay.append(delay_made)
        return 1 + (1 / sum(delay))

    def update_best_solution(self):
        for i in range(self.num_food_sources):
            fitness = self.fitness_value(self.working_matrix[i])
            if fitness > self.max_fitness:
                self.max_fitness = fitness
                self.best_solution = self.working_matrix[i][:]
                self.max_fitness_bee = i

    def select_two_random_numbers(self):
        return random.sample(range(0, self.num_jobs), 2)

    def swap(self, solution):
        i, j = self.select_two_random_numbers()
        solution[i], solution[j] = solution[j], solution[i]

    def insertion(self, solution):
        i, j = self.select_two_random_numbers()
        solution.insert(j, solution.pop(i))

    def reversion(self, solution):
        i, j = sorted(self.select_two_random_numbers())
        solution[i:j + 1] = reversed(solution[i:j + 1])

    def employed_bee_phase(self):
        for i in range(self.num_food_sources):
            new_solution = self.working_matrix[i][:]
            if random.random() < 1/3:
                self.swap(new_solution)
            elif random.random() < 2/3:
                self.insertion(new_solution)
            else:
                self.reversion(new_solution)

            if self.fitness_value(new_solution) > self.fitness_value(self.working_matrix[i]):
                self.working_matrix[i] = new_solution[:]

            self.q_table[tuple(self.working_matrix[i])] = self.fitness_value(self.working_matrix[i])
        
        self.update_best_solution()

    def onlooker_bee_phase(self):
        for _ in range(self.num_food_sources):
            selected_solution = max(self.working_matrix, key=lambda x: self.q_table[tuple(x)])
            new_solution = selected_solution[:]
            if random.random() < 1/3:
                self.swap(new_solution)
            elif random.random() < 2/3:
                self.insertion(new_solution)
            else:
                self.reversion(new_solution)

            if self.fitness_value(new_solution) > self.fitness_value(selected_solution):
                selected_solution = new_solution[:]
            
            self.q_table[tuple(selected_solution)] = self.fitness_value(selected_solution)
        
        self.update_best_solution()

    def scout_bee_phase(self):
        for i in range(self.num_food_sources):
            if self.fitness_value(self.working_matrix[i]) == self.max_fitness:
                self.working_matrix[i] = random.sample(range(1, self.num_jobs + 1), self.num_jobs)
                self.q_table[tuple(self.working_matrix[i])] = self.fitness_value(self.working_matrix[i])
        
        self.update_best_solution()

    def run(self):
        self.initialize()
        for _ in range(self.max_iterations):
            self.employed_bee_phase()
            self.onlooker_bee_phase()
            self.scout_bee_phase()
        
        return self.best_solution, self.max_fitness

# Example usage:
job_durations = [2, 4, 3, 5, 2]
job_deadlines = [3, 6, 5, 10, 4]
num_jobs = len(job_durations)
num_food_sources = 10
max_iterations = 100

abc = ArtificialBeeColony(num_jobs, job_durations, job_deadlines, num_food_sources, max_iterations)
best_solution, best_fitness = abc.run()

print(f"Best Solution: {best_solution}")
print(f"Best Fitness: {best_fitness}")
