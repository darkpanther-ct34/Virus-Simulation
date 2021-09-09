# importing the required modules
import matplotlib.pyplot as plt
import numpy as np
import virusSimulation as Vs


def main():
    simulation_length = 100
    num_of_starting_infected = 1
    population_size = 500

    y, y2 = Vs.run(simulation_length, num_of_starting_infected, population_size)

    # x axis values
    x = np.arange(simulation_length)

    # plotting the points
    plt.plot(x, y, label="virus cases")

    plt.plot(x, y2, label="vaccinations")

    # naming the x axis
    plt.xlabel('Num of Days')
    # naming the y axis
    plt.ylabel('% infected')

    # setting y axis range
    plt.ylim(1, 100)
    plt.xlim(1, simulation_length)
    # giving a title to my graph
    plt.title('Data')

    plt.legend()

    # function to show the plot
    plt.show()


if __name__ == '__main__':
    main()
