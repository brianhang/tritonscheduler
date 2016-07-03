#!/usr/bin/env python

from schedule import Schedule
from classparser import ClassParserError
from algorithm import Algorithm
from time import sleep

import pprint

# Whether or not debug input will be used.
DEBUG = False

# Various parameters for the genetic algorithm.
CAPACITY = 64
CROSSOVER = 0.02
MUTATE = 0.01
ELITISM = 0.1
GENERATIONS = 256

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
                    courses.append(course.upper())
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

    # Send the user input to the main function.
    info["term"] = term.upper()
    info["courses"] = courses

    return False

def main():
    """
    The main function of the program that turns user input into a schedule and
    uses a genetic algorithm to find an optimal schedule.
    """
    # Container for user input.
    info = {}

    # Get the desired term and courses.
    if DEBUG:
        info["term"] = "FA16"
        info["courses"] = ["CSE 12", "CSE 15L", "DOC 1"]
    elif handleInput(info):
        return

    print("Finding schedule data...")

    # Get the schedule data for the given courses and term.
    schedule = Schedule()
    schedule.term = info["term"]
    schedule.courses = info["courses"]

    try:
        scheduleData = schedule.retrieve()
    except ClassParserError: 
        print("The Schedule of Classes data could not be loaded at this " \
              "or you have provided an invalid class.")

        return
    
    # Make sure all of the desired classes were found.
    for course in info["courses"]:
        if course not in scheduleData:
            print("'" + course + "' was not found in the Schedule of Classes!")

            return

    # Initiate the population.
    algorithm = Algorithm(scheduleData)
    algorithm.initiate(CAPACITY, CROSSOVER, MUTATE, ELITISM)

    # Run the algorithm through the desired number of generations.
    generation = 0
    highest = 0


    while generation < GENERATIONS:
        algorithm.evolve()
        generation += 1

        print("Generating... "
              + str(int((generation / GENERATIONS) * 100)) + "%", end="\r")

    print("\nDone!")

    algorithm.printFittest()

if __name__ == "__main__":
    main()
