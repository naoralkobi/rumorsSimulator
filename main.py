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
    prefix_sum = []
    running_sum = 0
    for i in range(len(info)):
        running_sum += info[i]
        prefix_sum.append(running_sum)
    percent_know = [num / number_of_persons * 100 for num in prefix_sum]

    fig = plt.gcf()
    plt.plot(percent_know, color='r')
    plt.xlabel("generation")
    plt.ylabel("Infected population")
    plt.title(simulation_name)
    plt.show(block=True)
    user_answer = ''
    # asking the user if he wants to save the plot
    while user_answer != 'y' and user_answer != 'n':
        answer = input("Do you want to save " + simulation_name + " plot into PDF file? (y/n)\n")
        user_answer = answer.lower()
        if user_answer == "stop":
            quit()
        if user_answer != "y" and user_answer != "n":
            print("Please only enter y or n")
    if user_answer == 'y':
        # saves the plot into pdf file with the name of the simulation
        path = simulation_name.replace(":", "-")
        fig.savefig(path + ".pdf")


def main():
    # gets the simulations parameters from the csv file
    simulations_parameters = read_parameters()
    s = Simulation(simulations_parameters)
    # initialize all pygame parameters
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rumors Simulation")
    large_font = pygame.font.SysFont('comicsans', 35)
    small_font = pygame.font.SysFont('comicsans', 13)
    # simulate the simulation and getting the information of the simulation
    info = s.simulate(win, large_font, small_font)
    if info is None:
        return
    # plot the simulation into a plot
    plot_info(simulations_parameters.get("name"), info, s.number_of_persons)
    pygame.quit()


if __name__ == '__main__':
    main()
