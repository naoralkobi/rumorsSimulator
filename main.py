# in order to create exe file pyinstaller --onefile infectionSimulator.py
import sys
import subprocess
import pkg_resources
import os
import pygame
import matplotlib.pyplot as plt
import csv
import random
import time
from Simulator import Simulation, WIDTH, HEIGHT

required = {'tqdm', 'matplotlib', 'pygame'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout = subprocess.DEVNULL)
else:
    print("not missing")
os.system('cls' if os.name == 'nt' else 'clear')


def read_parameters():
    parameters = dict()
    # Todo add option to read from a file.;
    if not parameters:
        # this is default parameters
        parameters = {
            "p_population_density": 0.75,
            "p_s1": 0.2,
            "p_s2": 0.3,
            "p_s3": 0.4,
            "p_s4": 0.1,
            "l_generation": 2,
            "name": "default simulation"
        }
    return parameters


def plot_info(simulation_name, info, number_of_persons):
    """
    Generates a plot of the percentage of the infected population over time and saves it as a pdf file if the user requests.

    Args:
        simulation_name (str): The name of the simulation.
        info (list): A list of integers representing the number of infected people in each generation of the simulation.
        number_of_persons (int): The number of persons in the simulation.

    Returns:
        None
    """
    prefix_sum = [sum(info[:i+1]) for i in range(len(info))]
    percent_know = [num / number_of_persons * 100 for num in prefix_sum]

    fig = plt.gcf()
    plt.plot(percent_know, color='r')
    plt.xlabel("generation")
    plt.ylabel("Infected population")
    plt.title(simulation_name)
    plt.show(block=True)

    user_answer = ''
    while user_answer not in ('y', 'n'):
        answer = input("Do you want to save " + simulation_name + " plot into PDF file? (y/n)\n")
        user_answer = answer.lower()
        if user_answer == "stop":
            quit()
        if user_answer not in ('y', 'n'):
            print("Please only enter y or n")

    if user_answer == 'y':
        path = simulation_name.replace(":", "-")
        fig.savefig(path + ".pdf")


def main():
    """Runs the main simulation.

    Reads the simulation parameters from a CSV file, initializes a Simulation object and runs the simulation using
    Pygame. Once the simulation is completed, the results are plotted using Matplotlib.

    Returns:
        None
    """
    # Get the simulation parameters from the CSV file
    simulations_parameters = read_parameters()

    # Initialize the simulation
    s = Simulation(simulations_parameters)

    # Initialize Pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rumors Simulation")

    # Set fonts for the Pygame window
    large_font = pygame.font.SysFont('comicsans', 35)
    small_font = pygame.font.SysFont('comicsans', 13)

    # Run the simulation and get the information about it
    info = s.simulate(win, large_font, small_font)

    # If the simulation has no information, return
    if info is None:
        return

    # Plot the simulation results using Matplotlib
    plot_info(simulations_parameters.get("name"), info, s.number_of_persons)

    # Quit Pygame
    pygame.quit()


if __name__ == '__main__':
    main()
