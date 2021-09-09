import matplotlib.pyplot as plt
import random
import numpy as np


def run(sim_length, sim_num_of_starting_infected, pop_size):

    # variables that are used in the simulation and will be changed for different scenarios

    # The immunity time is the number of time a person is immune once they have recovered from the disease
    immunity_time = 3
    immunity = True

    # The infection rate is 1/x where x is infection_rate for each infectious person met
    infection_rate = 5000

    # The amount of time someone has the virus for
    infection_time = 12

    # The number of buildings that people can go to
    number_of_buildings = 50

    # The number of buildings someone visits in a day
    building_visits = 3

    vaccinations = True

    vaccination_rate = 10

    vaccination_start = 10

    virus_data = []
    vaccine_data = []

    class Person:
        def __init__(self, building, infected, resistant, vaccinated=False):
            self.building = building
            self.infected = infected
            self.resistant = resistant
            self.vaccinated = vaccinated
            self.time_since_infection = 0
            self.time_had_infection = 0
            self.people_infected = 0
            self.times_infected = int(infected)

        def infect(self, num_of_infectious_people):
            if not self.infected and not self.resistant and not self.vaccinated and not num_of_infectious_people == 0:
                num = random.randint(0, infection_rate)
                if num in range(0, num_of_infectious_people):
                    self.infected = True
                    self.times_infected += 1

        def next_day(self):
            if self.resistant and immunity:
                if self.time_since_infection == immunity_time:
                    self.resistant = False
                    self.time_since_infection = 0
                self.time_since_infection += 1
            if self.infected:
                self.time_had_infection += 1
                if self.time_had_infection == infection_time:
                    self.infected = False
                    self.time_had_infection = 0
                    if immunity:
                        self.resistant = True

        def pick_building(self):
            self.building = random.randint(0, number_of_buildings)

        def vaccinate(self):
            random_num = random.randint(0, vaccination_rate)
            if random_num in range(0, 1) and vaccinations:
                self.vaccinated = True

    def get_percent_infected(pop):
        num_infected = 0
        for person_inner in pop:
            num_infected += person_inner.infected
        return (num_infected / pop_size) * 100

    def get_percent_vaccinated(pop):
        num_vaccinated = 0
        for person_inner in pop:
            num_vaccinated += person_inner.vaccinated
        return (num_vaccinated / pop_size) * 100

    def get_r_rate(pop):
        average_r = []
        test = 0
        second_test = 0
        for person_inner in pop:
            if person_inner.times_infected > 0:
                add = person_inner.people_infected/person_inner.times_infected
                test += person_inner.people_infected
                second_test += person_inner.times_infected
                average_r.append(add)
        total = 0
        for infected in average_r:
            total += infected
        if len(average_r) > 0:
            total = total/len(average_r)
        return total

    population = []

    for i in range(pop_size-sim_num_of_starting_infected):
        new_person = Person(None, False, False)
        population.append(new_person)

    for i in range(sim_num_of_starting_infected):
        new_person = Person(None, True, False)
        population.append(new_person)

    print(f'population: {pop_size} \npercent infected: {(sim_num_of_starting_infected/ pop_size) * 100}'
          f'\nsimulation time: {sim_length}\ninfection rate: 1/{infection_rate}\nvaccination rate: 1/{vaccination_rate}'
          f'\nvaccination start: {vaccination_start}\nvaccinations: {vaccinations}\nimmunity: {immunity}')
    for i in range(sim_length):
        for j in range(building_visits):
            for person in range(pop_size):
                population[person].pick_building()
            for build in range(number_of_buildings):
                in_building = []
                num_infect = 0
                infected_index = []
                for person in range(pop_size):
                    if population[person].building == build:
                        in_building.append(population[person])
                        if population[person].infected:
                            num_infect += 1
                            infected_index.append(person)
                split = 0
                for person in population:
                    already = person.infected
                    person.infect(num_infect)
                    if person.infected and not already:
                        if split > len(infected_index)-1:
                            split = 0
                        population[infected_index[split]].people_infected += 1
                        split += 1
        for person in population:
            person.next_day()
        virus_data.append(get_percent_infected(population))
        vaccine_data.append(get_percent_vaccinated(population))
        if i > vaccination_start:
            for person in population:
                person.vaccinate()
    print("R-rate : ", get_r_rate(population))
    return virus_data, vaccine_data
