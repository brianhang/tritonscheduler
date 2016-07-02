#!/usr/bin/env python

from schedule import Schedule
from parser import ParserError
from algorithm import Algorithm
from time import sleep

import pprint

DEBUG = True

def handleInput(info):
    """
    Handles prompting for user input and validating user input. The results of
    valid input are stored in the info dictionary.

    :param info: where user input is stored
    :returns: whether or not the program should close
    """
    term = None

    # Get which term will be used.
    try:
        term = input("Enter your desired term (example: FA16): ")
    except:
        print("")

        return True

    # Validate the format of the term.
    while not Schedule.validateTerm(term):
        term = input("You have entered an invalid term, try again: ")

    # Get all the desired courses.
    print("Enter all of your desired classes on a separate line.")
    print("To finish entering classes, input an empty line.")

    courses = []

    while True:
        try:
            course = input()

            if course:
                if Schedule.validateCourse(course):
                    courses.append(course)
                else:
                    print("'" + course + "' is not a valid course code.")
            else:
                break
        except KeyboardInterrupt:
            return True
        except:
            break

    # Validate if any courses were entered.
    if len(courses) == 0:
        print("You did not enter any courses.")

        return True

    # Get the desired population size.
    size = 0

    try:
        size = int(input("Enter your desired population size: "))

        if size <= 0:
            print("You must enter a positive number.")

            raise ValueError()
    except ValueError:
        while True:
            try:
                size = int(input("You have entered an invalid size, " \
                                 "try again: "))

                if size <= 0:
                    print("You must enter a positive number.")
                else:
                    break
            except ValueError:
                continue
            except:
                return True

    # Send the user input to the main function.
    info["term"] = term
    info["courses"] = courses
    info["size"] = size

    return False

def main():
    """
    The main function of the program that turns user input into a schedule and
    uses a genetic algorithm to find an optimal schedule.
    """
    info = {}

    # Get the desired term and courses.
    if DEBUG:
        info["term"] = "FA16"
        info["courses"] = ["VIS 1", "CSE 12", "CSE 15L", "DOC 1"]
        info["size"] = 75
        info["gen"] = 100
        info["crossover"] = 0.05
        info["mutate"] = 0.005
        info["elitism"] = 0.1
    elif handleInput(info):
        return

    print("Finding schedule data...")

    # Get the desired size of the population.
    # Get the desired number of generations.

    # Get the schedule data for the given courses and term.
    schedule = Schedule()
    schedule.term = info["term"]
    schedule.courses = info["courses"]

    try:
        scheduleData = schedule.retrieve()
    except ParserError: 
        print("The Schedule of Classes data could not be loaded at this " \
              "or you have provided an invalid class.")

        return
    
    for course in info["courses"]:
        if course not in scheduleData:
            print("'" + course + "' was not found in the Schedule of Classes!")

            return

    # Initiate the population.
    algorithm = Algorithm(scheduleData)
    algorithm.initiate(info["size"], info["crossover"], info["mutate"],
                       info["elitism"])

    # Run the algorithm through the desired number of generations.
    generation = 0

    while generation < info["gen"]:
        print("Generation " + str(generation + 1) + " :: Total Fitness - "
              + str(algorithm.getTotalFitness()) + " :: Fittest - "
              + str(algorithm.getHighestFitness()))

        algorithm.evolve()
        generation += 1

    algorithm.printFittest()

if __name__ == "__main__":
    main()
